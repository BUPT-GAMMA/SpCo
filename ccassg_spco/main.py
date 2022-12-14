import numpy as np
import argparse

from model import CCA_SSG, LogReg
from aug import random_aug
from dataset import load

import numpy as np
import torch as th
import torch.nn as nn
import warnings
import dgl
from sklearn.metrics import f1_score
import scipy.sparse as sp
import torch
from params import set_params

warnings.filterwarnings('ignore')

args = set_params()

# check cuda
if args.gpu != -1 and th.cuda.is_available():
    args.device = 'cuda:{}'.format(args.gpu)
else:
    args.device = 'cpu'
'''
## random seed ##
seed = args.seed
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
'''

own_str = args.dataname
print(own_str)

def sinkhorn(K, dist, sin_iter):
    # make the matrix sum to 1
    u = np.ones([len(dist), 1]) / len(dist)
    K_ = sp.diags(1./dist)*K
    dist = dist.reshape(-1, 1)
    ll = 0
    for it in range(sin_iter):        
        u = 1./K_.dot(dist / (K.T.dot(u)))
    v = dist /(K.T.dot(u))
    delta = np.diag(u.reshape(-1)).dot(K).dot(np.diag(v.reshape(-1)))
    return delta    

def plug(theta, num_node, laplace, delta_add, delta_dele, epsilon, dist, sin_iter, c_flag=False):
    C = (1 - theta)*laplace.A
    if c_flag:
        C = laplace.A
    K_add = np.exp(2 * (C*delta_add).sum() * C / epsilon)
    K_dele = np.exp(-2 * (C*delta_dele).sum() * C / epsilon)
    
    delta_add = sinkhorn(K_add, dist, sin_iter)
    
    delta_dele = sinkhorn(K_dele, dist, sin_iter)
    return delta_add, delta_dele

def update(theta, epoch, total):
    theta = theta - theta*(epoch/total)
    return theta
    
def normalize_adj(adj):
    """Symmetrically normalize adjacency matrix."""
    adj = sp.coo_matrix(adj)
    rowsum = np.array(np.abs(adj.A).sum(1))
    d_inv_sqrt = np.power(rowsum, -0.5).flatten()
    d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.
    d_mat_inv_sqrt = sp.diags(d_inv_sqrt)
    return adj.dot(d_mat_inv_sqrt).transpose().dot(d_mat_inv_sqrt).tocoo()

def preprocess_features(features):
    """Row-normalize feature matrix and convert to tuple representation"""
    rowsum = np.array(features.sum(1))
    r_inv = np.power(rowsum, -1).flatten()
    r_inv[np.isinf(r_inv)] = 0.
    r_mat_inv = sp.diags(r_inv)
    features = r_mat_inv.dot(features)
    if isinstance(features, np.ndarray):
        return features
    else:
        return features.todense(), sparse_to_tuple(features)
        
def get_dataset(path, dataname, scope_flag):
    adj = sp.load_npz(path+"/adj.npz")
    
    feat = sp.load_npz(path+"/feat.npz").A
    if dataname!='blog':
        feat = torch.Tensor(preprocess_features(feat))
    else:
        feat = torch.Tensor(feat)
    num_features = feat.shape[-1]
    label = torch.LongTensor(np.load(path+"/label.npy"))
    idx_train20 = np.load(path+"/train20.npy")
    idx_train10 = np.load(path+"/train10.npy")
    idx_train5 = np.load(path+"/train5.npy")
    idx_train = [idx_train5, idx_train10, idx_train20]
    idx_val = np.load(path+"/val.npy")
    idx_test = np.load(path+"/test.npy")
    num_class = label.max()+1
    
    laplace = sp.eye(adj.shape[0]) - normalize_adj(adj)
    if scope_flag == 1:
        scope = torch.load(path+"/scope_1.pt")
    if scope_flag == 2:
        scope = torch.load(path+"/scope_2.pt")
    return adj, feat, label, num_class, idx_train, idx_val, idx_test, laplace, scope
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='cuda:2')


if __name__ == '__main__':

    print(args)
    path = "../dataset/"+args.dataname
    adj, feat, labels, num_class, train_idx, val_idx, test_idx, laplace, scope = get_dataset(path, args.dataname, args.scope_flag)
    adj = adj + sp.eye(adj.shape[0])
    graph = dgl.from_scipy(adj)
    
    if args.dataname=='pubmed':
        new_adjs = []
        for i in range(10):
            new_adjs.append(sp.load_npz(path+"/0.01_1_"+str(i)+".npz"))
        adj_num = len(new_adjs)
        adj_inter = int(adj_num / args.num)
        sele_adjs = []
        for i in range(args.num+1):
            try:
                if i==0:
                    sele_adjs.append(new_adjs[i])
                else:
                    sele_adjs.append(new_adjs[i*adj_inter-1])
            except IndexError:
                pass
        print("Number of select adjs:", len(sele_adjs))
        epoch_inter = args.epoch_inter
    else:
        scope_matrix = sp.coo_matrix((np.ones(scope.shape[1]), (scope[0, :], scope[1, :])), shape = adj.shape).A
        dist = adj.A.sum(-1) / adj.A.sum()
    
    in_dim = feat.shape[1]

    model = CCA_SSG(in_dim, args.hid_dim, args.out_dim, args.n_layers, args.use_mlp)
    model = model.to(args.device)

    optimizer = th.optim.Adam(model.parameters(), lr=args.lr1, weight_decay=args.wd1)

    N = graph.number_of_nodes()
    
    #### SpCo ######
    theta = 1
    delta = np.ones(adj.shape) * args.delta_origin
    delta_add = delta
    delta_dele = delta
    num_node = adj.shape[0]
    range_node = np.arange(num_node)
    ori_graph = graph
    new_graph = ori_graph
    
    new_adj = adj.tocsc()
    ori_attr = torch.Tensor(new_adj[new_adj.nonzero()])[0]
    ori_diag_attr = torch.Tensor(new_adj[range_node, range_node])[0]
    new_attr = torch.Tensor(new_adj[new_adj.nonzero()])[0]
    new_diag_attr = torch.Tensor(new_adj[range_node, range_node])[0]
    
    for epoch in range(args.epochs):
        model.train()
        optimizer.zero_grad()

        graph1_, attr1, feat1 = random_aug(new_graph, new_attr, new_diag_attr, feat, args.dfr, args.der)
        graph2_, attr2, feat2 = random_aug(ori_graph, ori_attr, ori_diag_attr, feat, args.dfr, args.der)
            
        graph1 = graph1_.to(args.device)
        graph2 = graph2_.to(args.device)
        
        attr1 = attr1.to(args.device)
        attr2 = attr2.to(args.device)
        
        feat1 = feat1.to(args.device)
        feat2 = feat2.to(args.device)
        z1, z2 = model(graph1, feat1, attr1, graph2, feat2, attr2)

        c = th.mm(z1.T, z2)
        c1 = th.mm(z1.T, z1)
        c2 = th.mm(z2.T, z2)

        c = c / N
        c1 = c1 / N
        c2 = c2 / N

        loss_inv = -th.diagonal(c).sum()
        iden = th.tensor(np.eye(c.shape[0])).to(args.device)
        loss_dec1 = (iden - c1).pow(2).sum()
        loss_dec2 = (iden - c2).pow(2).sum()

        loss = loss_inv + args.lambd * (loss_dec1 + loss_dec2)
        if torch.isnan(loss) == True:
            break
            
        loss.backward()
        optimizer.step()

        print('Epoch={:03d}, loss={:.4f}'.format(epoch, loss.item()))
        if args.dataname == 'pubmed':
            if (epoch-1) % epoch_inter == 0:
                try:
                    print("================================================")
                    delta = args.lam * sele_adjs[int(epoch / epoch_inter)]
                    new_adj = adj +  delta
                    
                    new_graph = dgl.from_scipy(new_adj)   
                    new_attr =  torch.Tensor(new_adj[new_adj.nonzero()])[0]   
                    new_diag_attr = torch.Tensor(new_adj[range_node, range_node])[0]   
                except IndexError:
                    pass
        else:
            if epoch % args.turn ==0:
                print("================================================")
                if args.dataname in ["cora", "citeseer"] and epoch!=0:
                    delta_add, delta_dele = plug(theta, num_node, laplace, delta_add, delta_dele, args.epsilon, dist, args.sin_iter, True)
                else:
                    delta_add, delta_dele = plug(theta, num_node, laplace, delta_add, delta_dele, args.epsilon, dist, args.sin_iter)
                delta = (delta_add - delta_dele)* scope_matrix
                delta = args.lam * normalize_adj(delta)
                new_adj = adj +  delta
                
                new_graph = dgl.from_scipy(new_adj)
                new_attr =  torch.Tensor(new_adj[new_adj.nonzero()])[0]
                new_diag_attr = torch.Tensor(new_adj[range_node, range_node])[0]
                theta = update(1, epoch, args.epochs) 
                
    print("=== Evaluation ===")
    graph = graph.to(args.device)
    graph = graph.remove_self_loop().add_self_loop()
    feat = feat.to(args.device)
    
    new_adj = graph.adj(scipy_fmt='coo').tocsc()
    attr = torch.Tensor(new_adj[new_adj.nonzero()])[0].to(args.device)
    embeds = model.get_embedding(graph, feat, attr)
    test_f1_macro_ll = 0
    test_f1_micro_ll = 0
    
    label_dict = {0:"5", 1:"10", 2:"20"}
    for i in range(3):
        train_embs = embeds[train_idx[i]]
        val_embs = embeds[val_idx]
        test_embs = embeds[test_idx]
    
        label = labels.to(args.device)
    
        train_labels = label[train_idx[i]]
        val_labels = label[val_idx]
        test_labels = label[test_idx]
    
        ''' Linear Evaluation '''
        logreg = LogReg(train_embs.shape[1], num_class)
        opt = th.optim.Adam(logreg.parameters(), lr=args.lr2, weight_decay=args.wd2)
    
        logreg = logreg.to(args.device)
        loss_fn = nn.CrossEntropyLoss()
    
        best_val_acc = 0
        eval_acc = 0
    
        for epoch in range(2000):
            logreg.train()
            opt.zero_grad()
            logits = logreg(train_embs)
            preds = th.argmax(logits, dim=1)
            train_acc = th.sum(preds == train_labels).float() / train_labels.shape[0]
            loss = loss_fn(logits, train_labels)
            loss.backward()
            opt.step()
    
            logreg.eval()
            with th.no_grad():
                val_logits = logreg(val_embs)
                test_logits = logreg(test_embs)
    
                val_preds = th.argmax(val_logits, dim=1)
                test_preds = th.argmax(test_logits, dim=1)
    
                val_acc = th.sum(val_preds == val_labels).float() / val_labels.shape[0]
                test_acc = th.sum(test_preds == test_labels).float() / test_labels.shape[0]
                
                test_f1_macro = f1_score(test_labels.cpu(), test_preds.cpu(), average='macro')
                test_f1_micro = f1_score(test_labels.cpu(), test_preds.cpu(), average='micro')
                if val_acc >= best_val_acc:
                    best_val_acc = val_acc
                    if test_acc > eval_acc:
                        test_f1_macro_ll = test_f1_macro
                        test_f1_micro_ll = test_f1_micro
    
                print('Epoch:{}, train_acc:{:.4f}, val_acc:{:4f}, test_acc:{:4f}'.format(epoch, train_acc, val_acc, test_acc))
    
        f=open(own_str+"_"+label_dict[i]+".txt", "a")
        f.write(str(test_f1_macro_ll)+"\t"+str(test_f1_micro_ll)+"\n")
        f.close()
