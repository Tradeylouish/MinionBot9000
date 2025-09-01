# MinionBot 9000

This 2019 project came about from procrastination on a 4th year Mechatronics Engineering computer vision assignment, by finding a far stupider application of computer vision -  making a minion that could identify bananas. It was only let outside once on a fortuitous minion-themed pub crawl, where it was my excuse not to wear a minion costume. Miraculously it survived the night, but it was hard to evaluate its banana recogintion performance over the sound of engineering students getting unreasonably drunk.

## Hardware 
Inside the minion plushy there is a cheap webcam ziptied to the inside of its goggle (monogle?), connected to a Raspberry Pi powered by a USB power bank. This is sufficient for running the banana recognition, but as an added extra there is an Arduino Uno feeding analog readings to the Pi over USB Serial, obtained via jupmer wires poking out of the minion's chest and hot-glued in place. Thus the minion's nipples act as a voltmeter, with a full bridge rectifier provided to allow bidirectional nipple clamping.

## Software
Because I could not be bothered taking many pictures of bananas, I took someone else's classifier model weights off the internet (I guess banana recognition is an established problem). The OpenCV Python package is used to apply the model to the webcam feed in real time, and pygame is used for controlling audio and making the minion say "banana" when it sees one.
This worked somewhat OK (good enough for me). The nipple-voltmeter is used as a volume control for pained minion noises, so that you (i.e. me) can torture the minion if you so desire.

## In action
https://github.com/user-attachments/assets/c53f564b-90a8-4860-b716-75e06acca9e3

https://github.com/user-attachments/assets/61f68290-d395-4cae-b11e-50ec3dd62a84

