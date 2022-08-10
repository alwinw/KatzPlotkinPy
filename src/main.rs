use std::f32::consts::PI;

fn main() {
    let epsilon = 0.15;
    let ak = 2.; // thickness coef [ND], 0-1
    let tl = 1.8; // T.E. angle coef [ND], 1-2
    let alpha = 0.; // angle of attack [deg]
    let m = 120; // number of panels

    let A = 2_f32 * tl * (epsilon + 1_f32).powf(ak - 1.) / ((2_f32).powf(ak));
    let al = alpha * PI / 180.;
    let itheta = 360 / m;

    let (mut x, mut y, mut cp): (f32, f32, f32);
    let (mut th, mut r1, mut r2, mut th1, mut th2, mut com1): (f32, f32, f32, f32, f32, f32);

    println!("{:>10}, {:>10}, {:>10}, {:>10}", "th", "x", "y", "cp");

    for i in (0..=360).step_by(itheta) {
        th = (i as f32) * PI / 180.;
        if i == 0 || i == 360 {
            x = 1.;
            y = 0.;
            cp = 1.;
            println!("{:10.6}, {:10.6}, {:10.6}, {:10.6}", th, x, y, cp);
            continue;
        }

        r1 = ((A * (th.cos() - 1.)).powi(2) + (A * th.sin()).powi(2)).sqrt();
        r2 = ((A * (th.cos() - epsilon)).powi(2) + (A * th.sin()).powi(2)).sqrt();

        th1 = (A * th.sin()).atan2(A * (th.cos() - 1.));
        th2 = (A * th.sin()).atan2(A * (th.cos() - epsilon));

        com1 = (r1.powf(ak) / r2.powf(ak - 1.))
            / (((ak - 1.) * th2).cos().powi(2) + ((ak - 1.) * th2).sin().powi(2));
        x = com1
            * ((ak * th1).cos() * ((ak - 1.) * th2).cos()
                + (ak * th1).sin() * ((ak - 1.) * th2).sin())
            + tl;
        y = com1
            * ((ak * th1).sin() * ((ak - 1.) * th2).cos()
                - (ak * th1).cos() * ((ak - 1.) * th2).sin());

        println!("{:10.6}, {:10.6}, {:10.6}, {:10.6}", th, x, y, 1);
    }
}
