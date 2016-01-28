#lang racket

(define (factorial x)
  (define (aux num acc)
    (cond
      ((= num 1)
       acc)
      (else
       (aux (sub1 num) (* acc num)))))
  (aux x 1))

(define num (string->number (vector-ref (current-command-line-arguments) 0)))

(void (factorial num))