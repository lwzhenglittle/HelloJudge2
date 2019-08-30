# 源程序文件名
SOURCE_FILE = "{filename}.hs"
# 输出程序文件名
OUTPUT_FILE = "{filename}.out"
# 编译命令行
COMPILE = "ghc -O2 {source} -o {output} {extra}"
# 运行命令行
RUN = 'sh -c "./{program} {redirect}"'
# 显示名
DISPLAY = "Haskell"
# 版本
VERSION = "GHC 8.0.2"
# Ace.js模式
ACE_MODE = "haskell"
