#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json


# In[6]:


def lambda_handler(event, context):
    return{
        'statusCode': 200,
        'body': json.dumps('hello world')
    }


# In[ ]:





# In[ ]:





# In[ ]:




