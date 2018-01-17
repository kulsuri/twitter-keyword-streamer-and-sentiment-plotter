# modules
import zmq
import datetime
import plotly.plotly as ply
import plotly.graph_objs as go
import plotly.tools as pls
from random import random
import pandas as pd
import os

# plotly stream token
stream_ids = pls.get_credentials_file()['stream_ids']
#print(stream_ids)

# set up connection to servers
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://10.50.0.119:4444')
socket.setsockopt_string(zmq.SUBSCRIBE, '')

# import tweet filter words
t = pd.read_csv(r'filter_names.csv')
filter_name = t['names'].tolist()

tweet_count = []
stream_id = []
token = []
trace = []
sent = []
st = []

# open data from plotly stream
for i in range(len(filter_name)):
    token.append(stream_ids[i])
    stream_id.append(dict(token=token[i]))
    sent.append(0)
    tweet_count.append(0)
    st.append(ply.Stream(stream_ids[i]))
    trace.append(go.Scatter(x=[], y=[], stream=stream_id[i], name=filter_name[i]))


# plot graphs
data = trace
layout = go.Layout(
    title='test title',
    yaxis=dict(
        title='sentiment'
    )
)
fig = go.Figure(data=data, layout=layout)
plot_url = ply.plot(fig, filename='stream_multiple_data')

for streams in st:
    streams.open()

while True:
    # receive data from server
    msg = socket.recv_string()
    # get the current time
    t = datetime.datetime.now()
    # get the filter name from data
    name = msg.split()[6]
    # split data in two
    for i in range(len(filter_name)):
        if name == filter_name[i]:
            # st[i].open()
            sent[i] += float(msg.split()[4])
            tweet_count[i] += 1
            # print(str(t) + ' | ' + str(sent[i]) + ' | ' + name)
            st[i].write({'x': t, 'y': float(sent[i])})
            os.system('cls')
            for i in range(len(filter_name)):
                print('{0}: Tweet Count: {1}. Sentiment: {2}.'
                      .format(filter_name[i], tweet_count[i], sent[i]))


# # plotly
# s = Stream(maxpoints=500, token=stream_ids[0])
# t1 = Scatter(x=[], y=[], name='tick data', mode='lines+markers', stream=s)
# t2 = Scatter(x=[], y=[], name='tick data', mode='lines+markers', stream=s)
# d = Data([t1, t2])
# l = Layout(title='Tick Data Stream')
# f = Figure(data=d, layout=l)
# ply.plot(f, filename='pokemon_live_plot', auto_open=True)
#
# st = ply.Stream(stream_ids[0])
# st.open()
#
# import numpy as np
#
# while True:
#     msg = socket.recv_string()
#     t1 = datetime.datetime.now()
#     #sym, value = msg.split()
#     value = msg
#     print('hello world')
#     print(str(t1) + '  |  ' + msg)
#     st.write({'x': t1, 'y': float(value)}) #, 'y2': np.random.randn(10)})

