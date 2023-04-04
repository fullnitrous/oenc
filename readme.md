# OENC

## Synopsis

Method for undetectably embedding arbitrary data into image.

## Details

Each pixel in the target image is made up of a tuple `(r, g, b)`,
`r`, `g, and `g` numbers ranging from 0 to 255. The data to be
embedded is considered as a bitstring.

For each bit in the data, if the bit is a one, the `r` value is
changed to the closest even number, if the bit is a zero the `r`
value is changed to the closes odd number. For the next bit the
`g` value is changed in a similar way. Three bits are stored
in each pixel. Procedure continues in width major order (row major order).
