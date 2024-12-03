#lang racket

(require advent-of-code)
(require test-engine/racket-tests)

(define EXAMPLE
#<<EXAMPLE
3   4
4   3
2   5
1   3
3   9
3   3
EXAMPLE
)

(define (get-aoc-input year day)
    (define (get-aocd-token)
        (define home (bytes->string/utf-8 (environment-variables-ref (current-environment-variables) #"HOME")))
        (define in (open-input-file (string-append home "/.config/aocd/token")))
        (define token (port->string in))
        (close-input-port in)
        token
    )
    (fetch-aoc-input (get-aocd-token) 2024 1 #:cache #t))

(define (parse-input input)

    (define (every-other lst)
        (let loop ([elements lst]
                   [acc empty])
            (cond [(null? elements) (reverse acc)]
                  [(null? (cdr elements)) (loop empty (cons (car elements) acc))]
                  [else (loop (cddr elements) (cons (car elements) acc))])))
    

    (define numbers (map string->number (regexp-match* #rx"[0-9]+" input)))
    (list (sort (every-other numbers) <) (sort (every-other (cdr numbers)) <)))

(check-expect (solve-p1 (parse-input EXAMPLE)) 11)
(define (solve-p1 input)
    (let loop ([left (car input)]
               [right (cadr input)]
               [acc 0])
        (cond [(or (null? left) (null? right)) acc]
              [else (loop (cdr left) (cdr right) (+ acc (abs (- (car left) (car right)))))])))

(check-expect (solve-p2 (parse-input EXAMPLE)) 31)
(define (solve-p2 input)

    (define (count-entries lst el)
        (foldr (lambda (x y) (+ y (if (eq? x el) 1 0))) 0 lst))

    (define (create-table left right)
        (make-hash (foldr (lambda (x y) (cons (list x (count-entries right x)) y)) empty left)))
    
    (define table (create-table (car input) (cadr input)))

    (foldr (lambda (x y) (+ y (* x (car (hash-ref table x))))) 0 (car input)))

(test)
(solve-p1 (parse-input (get-aoc-input 2024 1)))
(solve-p2 (parse-input (get-aoc-input 2024 1)))