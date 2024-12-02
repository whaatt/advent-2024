use std::cmp::Ordering;

fn main() {
    println!("{}", problem_1());
    println!("{}", problem_2());
}

fn problem_1() -> i32 {
    let mut count_safe = 0;
    let reports = get_reports();
    for report in reports {
        if report_is_safe(&report) {
            count_safe += 1;
        }
    }
    count_safe
}

fn problem_2() -> i32 {
    let mut count_safe = 0;
    let reports = get_reports();
    for report in reports {
        if report_is_safe(&report) {
            count_safe += 1;
            continue;
        }
        // Horrible...
        for (i, _) in report.iter().enumerate() {
            let mut report_altered: Vec<i32> = Vec::new();
            report_altered.extend_from_slice(&report[..i]);
            report_altered.extend_from_slice(&report[i + 1..]);
            if report_is_safe(&report_altered) {
                count_safe += 1;
                break;
            }
        }
    }
    count_safe
}

fn report_is_safe(report: &Vec<i32>) -> bool {
    let mut last: Option<i32> = None;
    let mut is_increasing: Option<bool> = None;
    for value in report {
        if last.is_some() {
            let diff = (value - last.unwrap()).abs();
            if !(1..=3).contains(&diff) {
                return false;
            }
        }
        match (last, is_increasing) {
            (Some(last_value), None) => match value.cmp(&last_value) {
                Ordering::Less => is_increasing = Some(false),
                Ordering::Greater => is_increasing = Some(true),
                Ordering::Equal => {
                    return false;
                }
            },
            (Some(last_value), Some(is_increasing_value)) => {
                match (value.cmp(&last_value), is_increasing_value) {
                    (Ordering::Less, true) => {
                        if is_increasing_value {
                            return false;
                        }
                    }
                    (Ordering::Greater, false) => {
                        if !is_increasing_value {
                            return false;
                        }
                    }
                    (Ordering::Equal, _) => {
                        return false;
                    }
                    _ => {}
                }
            }
            _ => {}
        }
        last = Some(*value);
    }
    true
}

fn get_reports() -> Vec<Vec<i32>> {
    let mut reports: Vec<Vec<i32>> = Vec::new();
    if let Ok(lines) = shared::read_lines("./2.txt") {
        for line in lines.map_while(Result::ok) {
            let ints: Vec<i32> = line.split(' ').map(|x| x.parse::<i32>().unwrap()).collect();
            reports.push(ints)
        }
    }
    reports
}
