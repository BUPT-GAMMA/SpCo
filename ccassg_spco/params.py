import argparse
import sys

argv = sys.argv
dataset = argv[1]

def cora_params():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--dataname', type=str, default="cora")    
    parser.add_argument('--gpu', type=int, default=0) 
    parser.add_argument('--lr1', type=float, default=1e-3)
    parser.add_argument('--lr2', type=float, default=1e-2)
    parser.add_argument('--wd1', type=float, default=0)
    parser.add_argument('--wd2', type=float, default=1e-4)
    parser.add_argument('--lambd', type=float, default=1e-3)
    parser.add_argument('--der', type=float, default=0.4)
    parser.add_argument('--dfr', type=float, default=0.1) 
    parser.add_argument('--use_mlp', action='store_true', default=False)
    parser.add_argument('--hid_dim', type=int, default=512)  
    parser.add_argument('--out_dim', type=int, default=512) 
    parser.add_argument('--n_layers', type=int, default=2)
    parser.add_argument('--seed', type=int, default=2)
    
    
    #####################################
    ## new parameters
    parser.add_argument('--delta_origin', type=float, default=0.5)
    parser.add_argument('--sin_iter', type=int, default=3) 
    
    parser.add_argument('--lam', type=float, default=0.5) 
    parser.add_argument('--epochs', type=int, default=40)
    parser.add_argument('--turn', type=int, default=15)
    parser.add_argument('--epsilon', type=float, default=0.01)
    parser.add_argument('--scope_flag', type=int, default=1)
    #####################################
    
    args, _ = parser.parse_known_args()
    return args
    
def citeseer_params():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--dataname', type=str, default="citeseer")    
    parser.add_argument('--gpu', type=int, default=0) 
    parser.add_argument('--lr1', type=float, default=1e-3)
    parser.add_argument('--lr2', type=float, default=1e-2)
    parser.add_argument('--wd1', type=float, default=0)
    parser.add_argument('--wd2', type=float, default=1e-2)
    parser.add_argument('--lambd', type=float, default=5e-4)
    parser.add_argument('--der', type=float, default=0.4)
    parser.add_argument('--dfr', type=float, default=0.0) 
    parser.add_argument('--use_mlp', action='store_true', default=False)
    parser.add_argument('--hid_dim', type=int, default=512)  
    parser.add_argument('--out_dim', type=int, default=512) 
    parser.add_argument('--n_layers', type=int, default=1)
    parser.add_argument('--seed', type=int, default=2)
    
    
    #####################################
    ## new parameters
    parser.add_argument('--delta_origin', type=float, default=0.5)
    parser.add_argument('--sin_iter', type=int, default=3)
    
    parser.add_argument('--lam', type=float, default=0.1) 
    parser.add_argument('--epochs', type=int, default=15)
    parser.add_argument('--turn', type=int, default=5)
    parser.add_argument('--epsilon', type=float, default=0.1)
    parser.add_argument('--scope_flag', type=int, default=1)
    #####################################
    
    args, _ = parser.parse_known_args()
    return args
    
def blog_params():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--dataname', type=str, default="blog")    
    parser.add_argument('--gpu', type=int, default=0) 
    parser.add_argument('--lr1', type=float, default=1e-3)
    parser.add_argument('--lr2', type=float, default=1e-2)
    parser.add_argument('--wd1', type=float, default=0)
    parser.add_argument('--wd2', type=float, default=1e-4)
    parser.add_argument('--lambd', type=float, default=1e-3)
    parser.add_argument('--der', type=float, default=0.5)
    parser.add_argument('--dfr', type=float, default=0.3) 
    parser.add_argument('--use_mlp', action='store_true', default=False)
    parser.add_argument('--hid_dim', type=int, default=512)  
    parser.add_argument('--out_dim', type=int, default=512) 
    parser.add_argument('--n_layers', type=int, default=2)
    parser.add_argument('--seed', type=int, default=2)
    
    
    #####################################
    ## new parameters
    parser.add_argument('--delta_origin', type=float, default=0.5)
    parser.add_argument('--sin_iter', type=int, default=3)
    
    parser.add_argument('--lam', type=float, default=0.1)   
    parser.add_argument('--epochs', type=int, default=75)
    parser.add_argument('--turn', type=int, default=10)
    parser.add_argument('--epsilon', type=float, default=0.1)
    parser.add_argument('--scope_flag', type=int, default=1)
    #####################################
    
    args, _ = parser.parse_known_args()
    return args
    
def flickr_params():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--dataname', type=str, default="flickr")    
    parser.add_argument('--gpu', type=int, default=0) 
    parser.add_argument('--lr1', type=float, default=1e-3)
    parser.add_argument('--lr2', type=float, default=1e-2)
    parser.add_argument('--wd1', type=float, default=0)
    parser.add_argument('--wd2', type=float, default=1e-4)
    parser.add_argument('--lambd', type=float, default=1e-3)
    parser.add_argument('--der', type=float, default=0.5)
    parser.add_argument('--dfr', type=float, default=0.3) 
    parser.add_argument('--use_mlp', action='store_true', default=False)
    parser.add_argument('--hid_dim', type=int, default=512)  
    parser.add_argument('--out_dim', type=int, default=512) 
    parser.add_argument('--n_layers', type=int, default=2)
    parser.add_argument('--seed', type=int, default=2)
    
    
    #####################################
    ## new parameters
    parser.add_argument('--delta_origin', type=float, default=0.5)
    parser.add_argument('--sin_iter', type=int, default=2)
    
    # 20 labeled nodes per class
    parser.add_argument('--lam', type=float, default=0.5) 
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--turn', type=int, default=30)
    parser.add_argument('--epsilon', type=float, default=0.01)
    parser.add_argument('--scope_flag', type=int, default=1)
    
    '''
    # 10 / 5 labeled nodes per class
    parser.add_argument('--lam', type=float, default=0.1) 
    parser.add_argument('--epochs', type=int, default=130)
    parser.add_argument('--turn', type=int, default=30)
    parser.add_argument('--epsilon', type=float, default=0.1)
    parser.add_argument('--scope_flag', type=int, default=1)
    '''
    #####################################
    
    args, _ = parser.parse_known_args()
    return args
    
def pubmed_params():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--dataname', type=str, default="pubmed")    
    parser.add_argument('--gpu', type=int, default=0) 
    parser.add_argument('--lr1', type=float, default=1e-3)
    parser.add_argument('--lr2', type=float, default=1e-2)
    parser.add_argument('--wd1', type=float, default=0)
    parser.add_argument('--wd2', type=float, default=1e-4)
    parser.add_argument('--lambd', type=float, default=1e-3)
    parser.add_argument('--der', type=float, default=0.5)
    parser.add_argument('--dfr', type=float, default=0.3) 
    parser.add_argument('--use_mlp', action='store_true', default=False)
    parser.add_argument('--hid_dim', type=int, default=512)  
    parser.add_argument('--out_dim', type=int, default=512) 
    parser.add_argument('--n_layers', type=int, default=2)
    parser.add_argument('--seed', type=int, default=2)
    
    
    #####################################
    ## new parameters
    parser.add_argument('--delta_origin', type=float, default=0.5)
    parser.add_argument('--theta', type=float, default=1.)  
    parser.add_argument('--sin_iter', type=int, default=1)
    
    # 20 / 10 labeled nodes per class
    parser.add_argument('--lam', type=float, default=0.1)
    parser.add_argument('--epochs', type=int, default=170)
    parser.add_argument('--num', type=int, default=7)
    parser.add_argument('--epoch_inter', type=int, default=15)
    parser.add_argument('--scope_flag', type=int, default=1)
    
    '''
    # 5 labeled nodes per class
    parser.add_argument('--lam', type=float, default=0.5)
    parser.add_argument('--epochs', type=int, default=150)
    parser.add_argument('--num', type=int, default=2)
    parser.add_argument('--epoch_inter', type=int, default=15)
    parser.add_argument('--scope_flag', type=int, default=1)
    '''
    #####################################
    
    args, _ = parser.parse_known_args()
    return args
    
def set_params():
    if dataset == "cora":
        args = cora_params()
    elif dataset == "citeseer":
        args = citeseer_params()
    elif dataset == "blog":
        args = blog_params()
    elif dataset == "flickr":
        args = flickr_params()
    elif dataset == "pubmed":
        args = pubmed_params()
    return args
