クライアントteachable machine(HTML+JavaScript)
-----------------------------
WebSocket通信:
    WebSocketオブジェクト生成("ws://127.0.0.1:30000")
    webSocket.onopen
       ソケット通信で接続が確立した時にopenイベントが発生し
       ここに設定したコールバック関数が呼び出される
    = function():
      「接続しました。」をshowのコンテナに追加
      WebSocket.onmessage
      　　　ソケット通信でサーバー側からのメッセージを受信した時にopenイベントが発生し、
      　　　ここに設定したコールバック関数が呼び出される
      = function(event):
           event.data でサーバーからの通知を受信
           event.data をshowコンテナに追加
      var sendMsg
      = function(val):
           var inputElement = msg IDのドキュメント要素を取得
           getElementById
           　　任意のHTMLタグで指定したIDにマッチするドキュメント要素を取得するメソッド
           inputElementの送信
           inputElementのクリア
------------------------------
Teachable Machine:
     const URL = teachable machineのURL

     コンストラクト:
          モデルの読み込み
          maxPredictions = クラスの総数を表す数値

          ウェブカメラをセットアップ
          幅200,高さ200,フリップtrue
          requestAnimationFrame()
               (自分自身の)処理を呼び出してループさせる

          canvasのセットアップ
          divの生成

    loop():
          ウェブカメラフレームの更新
          predict()の呼び出し
          requestAnimationFrame()

    predict():
          予測1：posenet「estimatePose」による入力は、画像、ビデオ、キャンバスのhtml要素を取り込むことができます。
          予測2：ティーチングマシン分類モデルによる入力の実行
          結果の出力
          drowpose()の呼び出し

    drowpose():







           　　
