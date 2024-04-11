# PDFのページを画像に変換するPythonスクリプト

指定したPDFのページを画像に変換します。

## 事前準備

Windows 11 Homeの環境でPython 3.11.2 64bit版で動作確認をしています。

### Pythonのインストール

お好きな方法でPythonをインストールしてください。

私は[`pyenv-win`](https://github.com/pyenv/pyenv-win)を使ってPython 3.11.2 64bit版をインストールしています。
[`pipenv`](https://pypi.org/project/pipenv/)も合わせてインストールします。

```bash
pyenv install 3.11.2
pyenv global 3.11.2
pip install pipenv
```

### Popplerのインストール

このコマンドで使用している[pdf2image](https://pypi.org/project/pdf2image/)が内部的に[Poppler](https://poppler.freedesktop.org/)を使用するので，事前にインストールしてください。

私はWindowsのMSYS2環境で以下のようにインストールしています。

```bash
pacman -S mingw-w64-x86_64-poppler mingw-w64-x86_64-poppler-data
```

### 必要なPythonパッケージのインストール

`pipenv`で必要なPythonパッケージをインストールします。

```
pipenv install
```

## 実行方法

入力PDFファイルを指定して実行します。他のコマンドライン引数を指定しなかった場合は以下と同じ動きになります。

```
pipenv run python pdf2img.py -o . -p 1 -f PNG -d 600 --prefix hoge hoge.pdf
```

カレントフォルダが`C:\home\saito`で，そのフォルダにある`hoge.pdf`を入力PDFにして上記のようにコマンドを実行した場合，以下のように表示されます。

```
Converting "hoge.pdf" to PNG...
  Page 1: C:\home\saito\hoge_1.png
Done!
```

### コマンドライン引数

コマンドライン引数の仕様は以下の通りです。

```
usage: pdf2img.py [-h] [-o OUTPUT_FOLDER] [-p PAGES] [-f {PNG,JPG}] [-d DPI] [--prefix PREFIX] pdf_path

PDFを指定された画像形式に変換する

positional arguments:
  pdf_path              入力PDFファイル

options:
  -h, --help            show this help message and exit
  -o OUTPUT_FOLDER, --output_folder OUTPUT_FOLDER
                        出力先フォルダ
  -p PAGES, --pages PAGES
                        出力するページ番号（カンマ区切りまたはハイフンで範囲指定可）
  -f {PNG,JPG}, --format {PNG,JPG}
                        画像の形式（PNG, JPG）
  -d DPI, --dpi DPI     画像のDPI
  --prefix PREFIX       出力画像ファイルのプレフィックス
```

* 出力先フォルダは指定しない場合はコマンドを実行したフォルダ（カレントフォルダ）になります。指定したフォルダが存在しない場合は作成します。
* 出力するページ番号はカンマ区切り（スペースは入れない）で複数のページを指定できます。  
  * 連続する複数ページを指定する場合は，\[開始ページ\]-\[終了ページ\]のようにハイフンでつないで指定することができます。  
    例：`-p 1,3-5,7`で1，3，4，5，7ページを出力します。
* 出力画像のプレフィックスは出力する画像のファイル名の最初に付く文字列です。指定しなかった場合は入力PDFファイルと同じになります。  
  * 出力画像のプレフィックに続いて，`_[ページ番号]`と指定した画像形式の拡張子（`.png`，`.jpg`）を付加します。  
  * 付加するページ番号は指定した最大ページ番号の桁数で0バディングされます。  
    例：`-p 1,100`の場合，ページ番号1が付加されるときに`_001`になります。
