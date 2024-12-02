use std::collections::HashMap;

fn main() {
    println!("{}", problem_1());
    println!("{}", problem_2());
}

fn problem_1() -> i32 {
    let (mut lefts, mut rights) = get_numbers();
    lefts.sort();
    rights.sort();
    let mut total = 0;
    for (i, _) in lefts.iter().enumerate() {
        total += (lefts[i] - rights[i]).abs();
    }
    total
}

fn problem_2() -> i32 {
    let (lefts, rights) = get_numbers();
    let mut counts: HashMap<i32, i32> = HashMap::new();
    for value in rights.iter() {
        *(counts.entry(*value).or_default()) += 1;
    }
    let mut total = 0;
    for value in lefts.iter() {
        total += value * *(counts.entry(*value).or_default())
    }
    total
}

fn get_numbers() -> (Vec<i32>, Vec<i32>) {
    let mut lefts: Vec<i32> = Vec::new();
    let mut rights: Vec<i32> = Vec::new();
    if let Ok(lines) = shared::read_lines("./1.txt") {
        for line in lines.map_while(Result::ok) {
            let ints: Vec<i32> = line
                .split("   ")
                .map(|x| x.parse::<i32>().unwrap())
                .collect();
            lefts.push(ints[0]);
            rights.push(ints[1]);
        }
    }
    (lefts, rights)
}
