# multiprocessing_echo_server
Python3で記述されたマルチプロセスで動作するエコーサーバです。  
[場阿忍愚CTF](https://burningctf.yamatosecurity.com/score/puzzle)の問題「164:電網術:Japanese kids are knowing」で使っています。  
※ところどころ雑なコードが残っています。  

this is Python3 code that is multiprocessing echo server.  
*there is still undesirable code  
  
## 使い方 
![使い方](https://raw.github.com/wiki/Euphoricwavism/multiprocessing_echo_server/images/multiprocessing_echo_server.gif)  
or  
```
$ python multiprocessing_echo_server.py 127.0.0.1 5006 20 "<C-D-E-F-E-D-C---E-F-G-A-G-F-E---C-C-C-C-CCDDEEFFE-D-C->Enter after encrypt your answer by MD5."
以下の通りでサーバを起動します
IPアドレス	：127.0.0.1
ポート		：5006
最大プロセス数	：20
エコー文言	：<C-D-E-F-E-D-C---E-F-G-A-G-F-E---C-C-C-C-CCDDEEFFE-D-C->Enter after encrypt your answer by MD5.
```

||第一引数|第二引数|第三引数|第四引数|  
|---|---:|---:|---:|---:|
|項目名|IPアドレス|解放ポート|最大コネクト数<br>（最大プロセス数）|エコー文字列|
|指定しない場合の<br>デフォルト値|0.0.0.0|56789|10|Hello world|