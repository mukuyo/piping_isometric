import ezdxf 
#新規のdxfを作成してバージョンを定義する
doc = ezdxf.new('R2010')
#モデルスペースを変数に定義する
msp = doc.modelspace() 
#モデルスペースに線を挿入
msp.add_line((0, 0), (10, 0))
#dxfを現在のディレクトリに保存
doc.saveas('./data/isometric/results/test.dxf')
