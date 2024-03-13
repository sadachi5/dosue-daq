#!/usr/bin/env python
import socket
import numpy as np
from time import sleep
import time
import matplotlib.pyplot as plt
import os, sys
import datetime

IP_ADDRESS = '10.10.10.5'
PORT = 18

def write(soc,word:str):
    word += '\n'
    #word += '\r\n'
    soc.send(word.encode())
    return 0;

# 説明
# write()は「文言word」をエンコードして送信する

def read(soc):
    ret_msg = ''
    i=0
    while True:
        print(f'i={i}')
        try:
            print('0');
            rcvmsg = soc.recv(1024).decode()
        except Exception as e:
            print(f'Error! {e}')
            soc.close()
            return None
        print('1');
        ret_msg += rcvmsg
        if rcvmsg[-1] == '\n':
        #if rcvmsg[-2:] == '\r\n':
            break        
        print('2');
        i=i+1
        pass
    print(f'read = {ret_msg}');
    return ret_msg.strip()

# 説明
# read()はデータを受信する関数。
# while Trueの無限ループでデータを受信し続ける
# 最大1024biteのデータを受信し、デコードしてrcvmsgに格納
# エラーハンドリング：try部分でexceptionがキャッチされた場合、エラー表示＆ソケット終了
# 受信したデータrcvmsgをret_msgに追加保存、データ蓄積
# データ終了条件の確認：受信したデータの最後の文字が「改行」であるかの確認。改行文字でない場合、ループは継続される。
# 完了：改行文字が確認されれば、受信を終える。ret_msgを返す。末尾の改行は消去。

def writeread(soc, word):
    print(f'writeread: {word}');
    write(soc, word)
    ret = read(soc)
    if ret is None :
        print('Error! Failed to read!')
        print('       --> Exit()')
        sys.exit(1)
        pass
    return ret;

# 説明
# wordを出力
# write()で「soc」にwordをエンコード＆送信
# read()でソケットsocからデータを受信
# エラーチェック：もしread()がNoneを返したら強制終了
# 正常に受信できたら、受信データをretとして保存


def read_data(soc):
    ut = time.time()
    rawstr = writeread(soc, 'READ:SAN?');
    if rawstr is None : return None;
    data = np.array([float(ns) for ns in rawstr.split(',')])
    return data[::2], data[1::2], ut

# 説明
# utに現在時刻を記録：UNIXタイムスタンプ
# writeread()で「READ:SAN?」コマンドを送信、データ受信、rawstrに保存
# エラーチェック：もしwriteread()がNoneを返したら、受信失敗でNoneを返す
# 処理：data配列から奇数番目と偶数番目の要素を取り出し、２つの別々の配列としてdata[::2]、data[1::2]に格納。


def test(freq) :
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    soc.connect((IP_ADDRESS, PORT))
    soc.settimeout(10)

    write(soc, '*CLS')
    write(soc, '*RST')
    print(writeread(soc, '*IDN?'));
    print(writeread(soc, ':SYST:COMM:LAN:CONF?'));

    print(writeread(soc, f':FREQ:FIX freq')) #これで周波数が調整できるはず
    print(writeread(soc, ))

#  上からちゃんと説明書読んでいかないと多分わかんない



    soc.close();

    return 0;

# 説明
# socketモジュールを使用して、IPv4 (socket.AF_INET) プロトコルを使用し、TCP (socket.SOCK_STREAM) ソケットを作成
# soc.connect((IP_ADDRESS, PORT)) を使用して、指定したIPアドレスとポート番号に接続
# 10秒以内にソケット操作が完了しないとタイムアウトエラー
# word[*CLS（クリア）][*RST（リセット）]をエンコード＆送信
# word[*IDN?][;SYST:COMM:LAN:CONF?]を送信、データを受信、printする

if __name__=='__main__':
    test();
    pass;

# Pythonスクリプトが直接実行された場合にのみ以下のコード部分が実行されるようにするためのコンディショナル（条件分岐）です。この構造を使用することで、スクリプトがモジュールとしてインポートされた場合には、そのまま実行されないようにすることができます。
