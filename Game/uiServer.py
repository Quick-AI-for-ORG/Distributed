
"""Import libraries"""
import os
import sys
from flask import Flask, request, jsonify, render_template

"""Import Folder Paths"""
sys.path.append(os.path.dirname("Buffer"))
sys.path.append(os.path.dirname("Entity"))
sys.path.append(os.path.dirname("Service"))
sys.path.append(os.path.dirname("Algorithm"))

from Entity.Player import Player
from Entity.Result import Result
app = Flask(__name__)
player = None
@app.route('/')
def main():
    return render_template('main.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/requestServer', methods=['POST'])
async def requestServer():
    player = Player(name=request.json.get('playerName'))
    gameSession = int(request.json.get('gameSession')) if request.json.get('gameSession') else None
    result = await player.requestServer(gameSession)
    print(result)
    result = Result.pbToObject(result.result)
    return jsonify({'isSuccess': result.isSuccess, 'message': result.message})



@app.route('/gameSettings')
def gameSettings():
    return render_template('settings.html')



if __name__ == '__main__':
    app.run(debug=True)
