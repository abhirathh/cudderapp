from django.urls import path
from . import views

urlpatterns = [
    path('passwords/<slug:username>', views.passwords, name = 'passwords'),
    path('get_chain', views.get_chain, name = 'get_chain'),
    path('mine_block/<slug:blocktitle>/<slug:cudder_username>/<slug:username>/<slug:password>', views.mine_block, name = 'mine_block'),
    path('get_user_blocks', views.get_user_blocks, name = 'get_user_blocks'),
    path('userCredentials', views.userCredentials, name = 'userCredentials'),
    path('get_data_chain', views.get_data_chain, name = 'get_data_chain'),
    path('mine_data_block/<slug:data_key>/<slug:cudder_username>/<slug:data_value>', views.mine_data_block, name = 'mine_data_block'),
    path('notes/<slug:username>', views.notes, name = 'notes'),
    path('storeData', views.storeData, name = 'storeData'),
    path('get_user_data_blocks', views.get_user_data_blocks, name = 'get_user_data_blocks'),
    path('chooseBroker', views.chooseBroker, name = 'chooseBroker'),
    path('apiConfData', views.apiConfData, name = 'apiConfData'),
    path('authUser', views.authUser, name = 'authUser',)
]
