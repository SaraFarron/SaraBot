### My first attempt at coding bots

[Telegram bot API docs](https://core.telegram.org/bots/api)

[aiogram docs](https://docs.aiogram.dev/en/latest/quick_start.html#simple-template)

## Telegram bot to improve vocabulary

### DONE

docker

### TODO

+ add/edit/delete words to/in/from db
+ upload xlsx/gsheets file with words to fill db
+ learn: algorithm to learn a pack of words
+ notifications to learn new words every day


### Plot of usage

start -> start buttons:
    learn new words -> select dictionary -> learning algorithm
    create new dictionary:
        dictionary name -> add words                   
    edit dictionary -> select dictionary -> buttons:
        add words
        update word -> search for word -> send updated version -> edit dictionary
    delete dictionary:
        select dictionary -> confirm -> start buttons 
    show dictionary:
        select dictionary -> (show) -> start buttons
    show learned words:
        (show) -> start buttons

funcs:
    add words:
        send file
        add word (/add [russian] [english]) -> add words
    cancel:
        (returns user to last stage of conversation, accessible anywhere)
