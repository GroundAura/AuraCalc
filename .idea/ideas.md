# AuraCalc Ideas

## Features

- [x] Exand window with expand button
- [x] change result element so it can't be typed in
- [x] add option to only evaluate when pressing enter or result button
- [ ] enter to move (expression,result) to memory and clear i/o
- [ ] up/down arrow keys to move through previous i/o
- [ ] viewable saved i/o
- [ ] save i/o history to file
- [x] button to clear i/o history
- [ ] random generation (whole or decimal)
- [-] dice rolling (ex 2d6-3), `roll(23d6-2)`
- [ ] various math functions
- [ ] long division (`ldiv(x,y)`, `longdiv(x,y)`, `x/%y`, `x//%y`)
- [x] #(#) to #*#
- [x] #^# to #**#
- [ ] remove newline character from result box, related to textbox height
- [ ] date calculation
- [ ] unit conversion

## Modes

- [ ] Angle mode (degrees/degrees:minutes:seconds/radians/gradients)
- [ ] Scientific notation or not
- [x] Exact or decimal approximation
- [x] Approximate constants (pi, e, etc.)
- [ ] which var to isolate ("Solve for var: [x]")

## Error Handling

- [x] log errors to console
- [x] log errors to AuraPy.log
- [ ] improve error messages

## Organization

- [x] separate functions into separate modules
- [ ] add docstrings for each function
- [ ] document possible operations

## Testing

- [ ] come up with edge cases to test

## Issues

<!--- `x^(y3+12)` => `x^(3y + 12)`
- `x^2(y3+12)` => `3x^2*(y + 4)`
- `x^(2(y3+12))` => `x^(6y + 24)`-->
- `roll(1d6)` -> `roll_dice(1*d*6)` => `ERROR: name 'd' is not defined`
- `root((x^3+3)-3,3)` => `(x^3)^(1/3)`, should be `x`
