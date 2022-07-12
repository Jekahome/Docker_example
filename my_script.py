import argparse
import os

# python my_script.py --my_var hello

print('ENV_VAR_NAME=',os.environ['ENV_VAR_NAME'])

parser = argparse.ArgumentParser()
parser.add_argument('--my_var', default=os.environ['ENV_VAR_NAME'], nargs='*', required=False)
  
args, unknown = parser.parse_known_args()
if args.my_var != None:
    my_var = str(args.my_var[0])
    print('my_var=',my_var)
    resource = open("/container_data/" + my_var ,'a+')
    resource.write(my_var)
    resource.close() 
else:
    print('my_var не задан')  
    
os.system("cd ../ && ls -l && cd container_data/ && ls -l") 


         
