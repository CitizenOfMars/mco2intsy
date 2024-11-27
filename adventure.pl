adjacent(X1, Y1, X2, Y2) :-
    (X2 is X1 + 1, Y2 = Y1); % Right
    (X2 is X1 - 1, Y2 = Y1); % Left
    (X2 = X1, Y2 is Y1 + 1); % Up
    (X2 = X1, Y2 is Y1 - 1). % Down

count_safe_adjacent(X, Y, Count) :-
    findall((A, B), (adjacent(X, Y, A, B), safe(A, B)), SafeCells),
    length(SafeCells, Count).