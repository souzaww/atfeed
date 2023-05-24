from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json, requests, xmltodict

from .database import Note, Queries, FeedParser


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            #usa função de Queries para adicionar a nota no banco de dados
            Queries.add_note_to_db(note, current_user.id)
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
    if request.method == 'POST': 
        #verifica o valor dos campos do formulário usando try/except
        try:
            name = request.form.get('name')
            feed_url = request.form.get('feed_url')
            print(name, feed_url)
        except:
            #mostra o detalhe do erro na página
            flash('Invalid form!', category='error')
            return render_template("feed.html", user=current_user)

        #valida se feed_url é uma url válida
        if feed_url[:4] != 'http':
            flash('Invalid URL!', category='error')
        elif len(name) < 1:
            flash('Feed name is too short!', category='error')
        else:
            #usa função de Queries para adicionar o feed no banco de dados
            Queries.add_feed_to_db(name, feed_url, current_user.id)
            flash('Feed added!', category='success')
            
    return render_template("feed.html", user=current_user)

# rota para ver detalhes do feed
@views.route('/feed/<int:feed_id>', methods=['GET', 'POST'])
@login_required
def feed_details(feed_id):
    #usa função de Queries para consultar o feed no banco de dados
    feed = Queries.get_feed_by_id(feed_id)
    return render_template("feed_details.html", user=current_user, feed=feed)

# rota para botão de "Process Feed"
@views.route('/feed/<int:feed_id>/process', methods=['GET', 'POST'])
@login_required
def process_feed(feed_id):
    if request.method == 'POST':
        #usa função de Queries para consultar o feed no banco de dados
        feed = Queries.get_feed_by_id(feed_id)
        feed_url = feed.feed_url
        #simula solicitação da página com user-agent de google chrome real
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \ AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(feed_url, headers=headers)
        content_type = response.headers['content-type']
        #verifica se o conteúdo é xml
        if content_type == 'application/xml':
            xml_data = response.content
            #transforma o xml em um dicionário
            data_dict = xmltodict.parse(xml_data)
            feed_items_data = data_dict['rss']['channel']['item']
            #itera sobre os itens do feed
            for item in feed_items_data[:5]:
                temp_item = {}
                #corrige nomes de tags com encode/decode
                temp_item['sku'] = item['g:id']
                temp_item['name'] = item['g:title']
                temp_item['price'] = item['g:price']
                temp_item['link'] = item['g:link']
                
                #armazena temp_item no banco de dados usando try/except
                try:
                    Queries.add_item_to_db(temp_item, feed_id)
                except:
                    print('Item already in database!')
            flash('Feed processed!', category='success')
            return redirect(url_for('views.feed_details', feed_id=feed_id))
        else:
            flash('Invalid feed!', category='error')
            return redirect(url_for('views.feed_details', feed_id=feed_id))



# @views.route('/delete-note', methods=['POST'])
# def delete_note():  
#     note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})
