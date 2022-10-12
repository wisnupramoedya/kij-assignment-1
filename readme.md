# Project API SocketIO Flask for Encryption

Created with :gift_heart: by Keluarga Kosimp

- [05111940000018 - Pramudya Tiandana Wisnu Gautama](https://github.com/wisnupramoedya)
- [05111940000062 - Thomas Felix Brilliant](https://github.com/ThomasFel)
- [05111940000096 - Stefanus Albert Kosim](https://github.com/yanzkosim)
- [05111940000175 - Muhammad Daffa](https://github.com/daffainfo)

## Requirements
- [MongoDB](https://www.mongodb.com/try/download/community)
- [NPM](https://nodejs.org/en/download/)
- [Python3](https://www.python.org/downloads/) or just use in the `Scripts` folder

## How to Prepare

1. Activate virtual env.
```
./Scripts/activate
```

2. Install the requirements needed.
```
pip install -r requirements.txt
```

3. If you want to create/update *requirements.txt*, add freeze.
```
pip3 freeze > requirements.txt
```

## How to Install Tailwind
1. Run npm install.
```
npm install
```

2. Install this PostCSS globally.
```
npm install --global postcss postcss-cli
```

Note:
- For some reason, there is a problem in loading automatics PostCSS in Tailwind. But, for every change, use this.
```
npx tailwindcss -i ./api/statics/src/main.css -o ./api/statics/dist/main.css --minify
```

## How to Run
1. Start the program.
```
./Scripts/python main.py
```

## API Documentation
The API is documented in Postman [here](https://documenter.getpostman.com/view/12334932/2s83zgtjKv).
