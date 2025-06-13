# Jupyter Notebook configuration for Docker environment

# Network settings
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.allow_root = True

# Security settings (開発環境用 - 本番環境では適切なトークンを設定してください)
c.NotebookApp.token = ''
c.NotebookApp.password = ''
c.NotebookApp.disable_check_xsrf = True

# ディレクトリ設定
c.NotebookApp.notebook_dir = '/app'

# 自動保存設定
c.FileContentsManager.checkpoints_kwargs = {'root_dir': '/tmp/.ipynb_checkpoints'}

# カーネル設定
c.MultiKernelManager.default_kernel_name = 'python3'

# ログ設定
c.NotebookApp.log_level = 'INFO'

# ファイル変更の監視
c.NotebookApp.contents_manager_class = 'notebook.services.contents.filemanager.FileContentsManager'

# 大きなファイルのサポート
c.NotebookApp.max_buffer_size = 2**30  # 1GB

# WebSocket設定
c.NotebookApp.allow_origin = '*'
c.NotebookApp.allow_credentials = True