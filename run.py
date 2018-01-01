from app import app
import os
port = int(os.environ['PORT'])
app.run(debug=False, host='0.0.0.0', port=port)
