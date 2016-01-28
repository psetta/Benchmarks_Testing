#lang racket

(define (factorial x)
  (cond
    ((zero? x) 1)
    (else
     (* x (factorial (sub1 x))))))

(define num (string->number (vector-ref (current-command-line-arguments) 0)))

(void (factorial num))