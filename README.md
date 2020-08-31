# PythonのProtocolとinjectorを組み合わせてみる勉強

## なぜこれをしようと思ったのか

[Python 3.9 時代の型安全な Pythonの極め方](https://speakerdeck.com/yamitzky/mastering-type-safety-in-python-3-dot-9-era) を読み、抽象クラスを使わずともProtocolを使うことで「必要なメソッドを持っているか」をPythonicな形でうまく表現できることを知った。

一方、PythonでDDDを実践していく中で、ドメイン層にレポジトリのインターフェイスを定義し、そのインターフェイスを実装した具体的なクラスをインフラストラクチャー層に実装するということをしている。その際、ドメイン層ではABC - Abstract Base Classesを使って抽象クラスを作る方法を取っていた。
ABCだとインターフェイスとその実装クラスの間に継承関係が発生するが、Protocolを使えば継承関係を持たせる必要がなくなる。

DDDでは[injector](https://pypi.org/project/injector/)を使いDIをしているが、ABCの時は上手く動いているが、Protocolを使ったときにinjectorがうまく動くか分からなかったので実験してみた。


## 環境
* Windows 10 version 2004 (OS Build 19041.450)
* Python 3.7.7
  * [Protocol](https://docs.python.org/ja/3/library/typing.html#typing.Protocol)
  * [typing-extensions 3.7.4.3](https://pypi.org/project/typing-extensions/)
  * [injector 0.18.3](https://pypi.org/project/injector/)
  * [mypy 0.782](https://pypi.org/project/mypy/)
* VSCode 1.47.3
* VSCode拡張機能
  * [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  * [Python Test Explorer for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=LittleFoxTeam.vscode-python-test-adapter)


## 環境構築方法

まずはPowershellを立ち上げ、普通にvenv作ってactivateする

```powershell
python3 -m venv venv
venv/Scripts/Activate.ps1
```

あとは、依存ライブラリをインストールする。

```
pip install -r requirements.txt
```


## 実装例

Procotolを使ったサンプルはsample_protocol.pyに書いた。

ABCを使ったサンプルはsample_abc.pyに書いた。


## 所感

injectorとProcotolを組み合わせた場合、Protocolで定義したメソッドが実装されていなかったとしても、その未実装メソッドが呼び出されるまではエラーにならない。

対して、injectorとABCを組み合わせた場合、`@abstractmethod`でアノテーションしたものが実装されていないと、インスタンス化される時点でエラーになる。

エラーの早期発見しやすさだとABCに軍配が上がるが、Protocol側でエラーの早期発見のための手立てはなにかあるのだろうか。
