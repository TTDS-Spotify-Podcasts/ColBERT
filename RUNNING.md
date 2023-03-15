# Running guideline

### Useful command for running instance at background
```
screen -S [NAME] # Create a screen with name
screen -r [NAME] # Connect to the targeted screen
```

When it's inside screen:
```
Ctrl-a + Esc # For scrolling in the terminal
Ctrl-a + d   # Deteached from the current screen terminal 
```
### Initialise colbert instance
```
screen -S colbert
conda activate colbert
cd ~/TTDS/ColBERT
bash bootstrap.sh
```
### Expose the searching to web
```
screen -S ngrok
cd ~/TTDS/ColBERT
bash ngrok.sh
```