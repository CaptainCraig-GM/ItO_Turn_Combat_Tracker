This is a simple enounter / combat tracker for Mark of the Odd games

How it works. Compile and run "TurnTracker.py" and you are faced with a window.

~ Top Left is a large text block area, lines get printed here
~ Bottom Left is the clock
~ Bottom Right is a SetTime button
~ Top Right is lots of fun buttons


SetTime button =
  > changes display to ask for an hour and a minute. 
  > Select an hour, and a 10 minute chunk of time.
  > Check off "Is Night?" if it is night time.
  > when set, the Bottom Left time should update.

add turn,  +hrs,  +turns and the text box
  add turn =
    > will advance the time forward by 10 minuts
    > there is an internal counter that will display Random Encounter results as time passes
       > Rolls for encounter every 3rd turn (or 2nd if 'in the Danger Zone' )
    
  +hrs =
    > looks for a number in the input field below
    > then quickly adds that many hours onto the clock.
    > it does not check for Random Encounters

  +turns =
    > looks for a number in the input field below...
    > then quickly adds that many 10 minute turns onto the clock
    > it does not check for Random Encounters

Enc. Check   and   Combat
  Enc. Check =
    > Spits out an Encounter Check with Range and Reaction if needed

  Combat =
    > Jumps over to Combat Tracker mode
    >>> More on that below

Timer Name,   Timer Turns   and   +tmr button
  These are used to track timed resources (Lanterns, Torches, Spell Effects...)
  Timer Name =
    > Put a name in the box to the right of the Timer Name label
      > Unique names help if you have a few timers on the go
    > Put a number of 10 minute turns in the box to the right of the Timer Turns label
    > Finally press the +tmr button
    >>> As turns are counted off, they will mention how many turns remain on each timer.

in the Danger Zone? toggle
  > The tracker checks for Random Encounters every 3rd turn.
  > if PCs are 'in the Danger Zone' it will check every second turn

Loot   and   Name
  > Loot gives some mundane crap that you may find on a body, fantasy themed
  > Name gives a random name, fantasy themed.

~-----~   Combat Tracker   ~-----~
Pressing the Combat button changes the screen to a combat tracker.
The window is broken up as so:
Up top:   three buttons and a text input field to put baddies onto the list
In Mid:   a list of the baddies in the encounter
Downlow:  A text field, dice rolling buttons, a Morale check, and an End Combat button

Starting Up top
make button =
  > checks the input field for a VERY SPECIFIC string.
    > if the string is wrong, nothing happens, but if the string is correct
  > add the contents of the string into the Baddie list as a new element.

This is what your string should look like:

Wyvern,beefy,10,2,15,9,7,2,d10 bite,d6b tail,Flies around like an asshole,Tail swipe inflicts Poison

it's a comma separated list, with the following elements:
Name,Description,hp,armour,Strength,Dexterity,Charisma,#OfAttacks,atkDesc,atkDesc,tagline,tagline,...
NOTES:
  > when parsing the string, I'm looking for commas to break it up into elements. Don't use commas in the tagLines
  > You can have as many tagLines as you want and this will parse and add them onto the Bottom
  > Don't put in more than two attacks: One is fine, two is fine. More causes errors.
    > on the same page, if you have 2 listed for #ofAttacks, make sure you have two atkDesc following it. 

file button =
prompts for a file location. I wan't a .txt file, with a bunch of lines like the string above.
  > use Lists/monList.txt as an example
  > the tracker will chow through them, and attempt to create a list element from each new line.
    > Best of Luck <

+Grunt button =
Drops a low life thug into the tracker
  > Random name, description and stats

In Mid:
If everything is working correctly, you should have a big beautiful list of all the baddies you are tracking.
You'll notice they have all the stats layed out nicely, and a few buttons on the right
  > The 1 or 2 attack buttons will roll the correct die into the text box on the Bottom
  > The hurt buutton looks into the upper input field for a number
    > if it finds it, it will remove that amount (minus the target's armour value) from the targets hp
    > when hp is reduced to 0, it then comes off the Strength score.
      > Whenever the Strength score is reduced, the tracker makes a roll to see if the target took critical damage]
      > if so, it displays it in the bottom text box.
  > The kill button just removes the monster from the list (and notes it in the text box)

Downlow:
the dice buttons just spit out a randon number up the the button pressed

Morale Button =
  > internally rolls a 2d6 test and states what type of enemies will take off.
    > I think of how the enemies are feeling before rolling (Hmm, they seem nervous)

End Combat =
  does just that. takes you back to the turn tracker screen
    > it keeps all your stuff though. Probably should have made a 'clear' button. oh well and have fun.