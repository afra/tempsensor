version(0.2);

/* board */
deep = 51;
long = 70;
board_margin = 0.2;

board_heigh = 7;
wall_heigh = 3;


/* add overlap around the board */
overlap = 2;

/* inner board overlap. The board lies on this */
inner = 3;

difference() {
    cube([long + 2*overlap, deep + 2*overlap, board_heigh + wall_heigh]);
    union() {
        translate([overlap + inner, overlap + inner, 0]) {
            color("red") {
                cube([long - inner*2, deep - inner*2, board_heigh]);
            }
        }
        translate([
                overlap - board_margin,
                overlap - board_margin,
                board_heigh]) {
            color("green") {
                cube([long + board_margin*2, deep + board_margin*2, wall_heigh]);
            }
        }
        /* remove most of the north side */
        translate([overlap + inner, deep - inner, 0]) {
            cube([40, deep, board_heigh + wall_heigh]);
        }
    }
}

/* support structur */
translate([0, 20, 0]) {
    cube([long + overlap*2, 2, 1]);
}
translate([
        overlap + inner + 40,
        overlap + board_margin + deep - 10,
        0]) {
     cube([long - inner - 40, 2, 1]);
     cube([2, 10, 1]);
}

/* board for optical verification */
/*
translate([overlap, overlap, 6]) {
    color("blue")
    cube([long, deep, 0.5]);
}
*/
