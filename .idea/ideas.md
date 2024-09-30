# AuraCalc Ideas

## Features

- [ ] Exand window with expand button
- [ ] change result element so it can't be typed in
- [ ] add option to only evaluate when pressing enter or result button
- [ ] enter to move (expression,result) to memory and clear i/o
- [ ] up/down arrow keys to move through previous i/o
- [ ] viewable saved i/o
- [ ] save i/o history to file
- [ ] button to clear i/o history
- [ ] random generation (whole or decimal)
- [ ] dice rolling (ex 2d6-3), `roll(23d6-2)`
- [ ] various math functions
- [ ] long division (`ldiv(x,y)`, `longdiv(x,y)`, `x/%y`, `x//%y`)
- [ ] #(#) to #*#
- [x] #^# to #**#
- [ ] remove newline character from result box, related to textbox height

## Error Handling

- [ ] log errors to console
- [ ] log errors to AuraPy.log
- [ ] improve error messages

## Organization

- [ ] separate functions into separate modules
- [ ] add docstrings for each function
- [ ] document possible operations

## Testing

- [ ] come up with edge cases to test

## Issues

<!--`x^(y3+12)` => `x^(3y + 12)`-->
<!--`x^2(y3+12)` => `3x^2*(y + 4)`-->
<!--`x^(2(y3+12))` => `x^(6y + 24)`-->
`roll(1d6)` -> `roll_dice(1*d*6)` => `ERROR: name 'd' is not defined`