import hashlib
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
import datetime
import json
from accounts.models import userApiConfig
from django.views.decorators.csrf import csrf_exempt

### Credentials Blockchain ###
class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(cudder_username = 'genesisUsername', blocktitle = 'genesisTitle', username = 'genesisUsername', hash = 'genesisHash', password = 'genesisPassword', previous_hash = '0')

    def create_block(self, blocktitle, cudder_username,username, hash, password, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'hash': hash,
                 'timestamp': str(datetime.datetime.now()),
                 'cudder_username': cudder_username,
                 'blocktitle': blocktitle,
                 'username': username,
                 'password': password,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash(self, username, password, cudder_username):
        encoded_hash = username + password + cudder_username
        return hashlib.sha256(encoded_hash.encode()).hexdigest()


# Creating our Blockchain
blockchain = Blockchain()

# Mining a new block
def mine_block(request, blocktitle, cudder_username, username, password):
    if cudder_username == request.user.username:
        previous_block = blockchain.get_previous_block()
        username = username
        password = password
        cudder_username = request.user.username
        previous_hash = blockchain.hash(previous_block['username'], previous_block['password'], previous_block['cudder_username'])
        block_hash = blockchain.hash(username, password, cudder_username)
        block = blockchain.create_block(blocktitle, cudder_username, username, block_hash, password, previous_hash)
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'hash': block['hash'],
                    'timestamp': block['timestamp'],
                    'blocktitle': blocktitle,
                    'cudder_username': cudder_username,
                    'username': block['username'],
                    'password': block['password'],
                    'previous_hash': previous_hash}
        return JsonResponse(response)
    else:
        err_json = {
        'status': 'failed',
        'reason': 'invalid user'
        }

        return JsonResponse(err_json)

# Getting the full Blockchain
def get_chain(request):
    if request.method == 'GET':
        response = {'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
    return JsonResponse(response)

def get_user_blocks(request):
    url = 'http://127.0.0.1:8000/blocks/get_chain'
    r = requests.get(url)
    data = r.json()
    user_data = []
    for v in data['chain']:
        if v['cudder_username'] == request.user.username:
            user_data.append(v)

    return JsonResponse(user_data, safe = False)


def passwords(request, username):
    if username == request.user.username:
        return render(request, 'blocks/passwords.html')
    else:
        return HttpResponse('Invalid user')

@csrf_exempt
def userCredentials(request):
    if request.method == 'POST':
        blocktitle = request.POST['blocktitle']
        username = request.POST['username']
        password = request.POST['password']

        mine_block(request, blocktitle, request.user.username, username, password)

        return redirect(f'/blocks/passwords/{request.user.username}')


### Notes Blockchain ###
class NotesBlockchain:

    def __init__(self):
        self.chain = []
        self.create_block(cudder_username = 'genesisUsername', blocktitle = 'genesisTitle', note = 'genesisNote' ,hash = 'genesisHash', previous_hash = '0')

    def create_block(self, blocktitle, cudder_username, note, hash, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'hash': hash,
                 'timestamp': str(datetime.datetime.now()),
                 'cudder_username': cudder_username,
                 'blocktitle': blocktitle,
                 'note': note,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash(self, note, cudder_username, timestamp):
        encoded_hash = note + cudder_username + timestamp
        return hashlib.sha256(encoded_hash.encode()).hexdigest()


# Creating our Blockchain
notesblockchain = NotesBlockchain()

# Mining a new block
def mine_note_block(request, blocktitle, cudder_username, note):
    if userApiConfig.objects.filter(username = cudder_username):
        print('Here')
        previous_block = notesblockchain.get_previous_block()
        note = note
        timestamp = str(datetime.datetime.now())
        # cudder_username = request.user.username
        previous_hash = notesblockchain.hash(previous_block['note'], previous_block['cudder_username'], previous_block['timestamp'])
        block_hash = notesblockchain.hash(note, cudder_username, timestamp)
        block = notesblockchain.create_block(blocktitle, cudder_username, note, block_hash, previous_hash)
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'hash': block['hash'],
                    'timestamp': block['timestamp'],
                    'blocktitle': blocktitle,
                    'cudder_username': cudder_username,
                    'note': block['note'],
                    'previous_hash': previous_hash}
        return JsonResponse(response)
    else:
        err_json = {
        'status': 'failed',
        'reason': 'invalid user'
        }

        return JsonResponse(err_json)

# Getting the full Blockchain
def get_notes_chain(request):
    if request.method == 'GET':
        response = {'chain': notesblockchain.chain,
                    'length': len(notesblockchain.chain)}
    return JsonResponse(response)

@csrf_exempt
def get_user_notes_blocks(request):
    if request.method == 'POST':
        cudder_username = request.POST['cudder_username']
        cudder_api_key = request.POST['cudder_api_key']

        if userApiConfig.objects.filter(username = cudder_username, api_key = cudder_api_key):
            url = 'http://127.0.0.1:8000/blocks/get_notes_chain'
            r = requests.get(url)
            data = r.json()
            user_data = []

            for v in data['chain']:
                if v['cudder_username'] == cudder_username:
                    user_data.append(v)

            return JsonResponse(user_data, safe = False)

        else:
            err_data_json = {'message': 'invalid user'}
            return JsonResponse(err_data_json)

def notes(request, username):
    if username == request.user.username:
        return render(request, 'blocks/notes.html')


@csrf_exempt
def userNotes(request):
    if request.method == 'POST':
        notetitle = request.POST['notetitle']
        note = request.POST['note']
        cudder_username = request.POST.get('cudder_username')
        cudder_api_key = request.POST.get('cudder_api_key')

        if userApiConfig.objects.filter(username = cudder_username, api_key = cudder_api_key):
            mine_note_block(request, notetitle, cudder_username, note)

            ret_json_data = {'message': 'block created'}
            return JsonResponse(ret_json_data)

        else:

            err_json_data = {'message': 'invalid user'}
            return JsonResponse(err_json_data)


def chooseBroker(request):
    return render(request, 'broker.html')


def apiConfData(request):
    if request.method == 'POST':
        pass
        # brokerSelect = request.POST.get('brokerSelect')
        # brokerUID = request.POST['brokerUID']
        # brokerApiKey = request.POST['brokerApiKey']
        # brokerSecretKey = request.POST['brokerSecretKey']
        #
        # userApiConfig.objects.create(
        # username = request.user.username,
        # broker = brokerSelect,
        # broker_user_id = brokerUID,
        # broker_api_key = brokerApiKey,
        # broker_secret_key = brokerSecretKey
        # )
        #
        # return redirect('/blocks/chooseBroker')


##########################

class DataBlockchain:

    def __init__(self):
        self.chain = []
        self.create_block(cudder_username = 'genesisUsername', data_key = 'genesisKey', data_value = 'genesisValue', hash = 'genesisHash', previous_hash = '0')

    def create_block(self, data_key, cudder_username, data_value, hash, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'hash': hash,
                 'timestamp': str(datetime.datetime.now()),
                 'cudder_username': cudder_username,
                 'data_key': data_key,
                 'data_value': data_value,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash(self, data_value, cudder_username, timestamp):
        encoded_hash = data_value + cudder_username + timestamp
        return hashlib.sha256(encoded_hash.encode()).hexdigest()


# Creating our Blockchain
datablockchain = DataBlockchain()

# Mining a new block
def mine_data_block(request, data_key, cudder_username, data_value):
    if userApiConfig.objects.filter(username = cudder_username):
        print('Heree')
        previous_block = datablockchain.get_previous_block()
        # note = note
        timestamp = str(datetime.datetime.now())
        # cudder_username = request.user.username
        previous_hash = datablockchain.hash(previous_block['data_value'], previous_block['cudder_username'], previous_block['timestamp'])
        block_hash = datablockchain.hash(data_value, cudder_username, timestamp)
        block = datablockchain.create_block(data_key, cudder_username, data_value, block_hash, previous_hash)
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'hash': block['hash'],
                    'timestamp': block['timestamp'],
                    'data_key': data_key,
                    'cudder_username': cudder_username,
                    'data_value': block['data_value'],
                    'previous_hash': previous_hash}
        print(response)
        return JsonResponse(response)
    else:
        err_json = {
        'status': 'failed',
        'reason': 'invalid user'
        }

        return JsonResponse(err_json)

# Getting the full Blockchain
def delete_data_block(request):
    pass

def get_data_chain(request):
    if request.method == 'GET':
        response = {'chain': datablockchain.chain,
                    'length': len(datablockchain.chain)}
    return JsonResponse(response)

@csrf_exempt
def get_user_data_blocks(request):
    if request.method == 'POST':
        cudder_username = request.POST['cudder_username']
        cudder_api_key = request.POST['cudder_api_key']

        if userApiConfig.objects.filter(username = cudder_username, api_key = cudder_api_key):
            url = 'http://127.0.0.1:8000/blocks/get_data_chain'
            r = requests.get(url)
            data = r.json()
            user_data = []

            for v in data['chain']:
                if v['cudder_username'] == cudder_username:
                    user_data.append(v)

            return JsonResponse(user_data, safe = False)

        else:
            err_data_json = {'message': 'invalid user'}
            return JsonResponse(err_data_json)


@csrf_exempt
def storeData(request):
    if request.method == 'POST':
        data_key = request.POST['key']
        data_value = request.POST['value']
        cudder_username = request.POST.get('cudder_username')
        cudder_api_key = request.POST.get('cudder_api_key')

        if userApiConfig.objects.filter(username = cudder_username, api_key = cudder_api_key):
            mine_data_block(request, data_key, cudder_username, data_value)

            ret_json_data = {'message': 'block created'}
            return JsonResponse(ret_json_data)

        else:

            err_json_data = {'message': 'invalid user'}
            return JsonResponse(err_json_data)


@csrf_exempt
def authUser(request):
    if request.method == 'POST':
        cudder_username = request.POST['cudder_username']
        cudder_api_key = request.POST['cudder_api_key']

        # print(cudder_username, cudder_api_key)

        if userApiConfig.objects.filter(username = cudder_username, api_key = cudder_api_key):
            success_data_res = {'auth': True, 'cudder_username': cudder_username, 'cudder_api_key': cudder_api_key}
            return JsonResponse(success_data_res)
        else:
            failure_data_res = {'auth': False}
            return JsonResponse(failure_data_res)
