%Usando operadores prolog.

:-op(100,xfx,eh).
:-op(90,fx,um).
:-op(90,fx,uma).

gimli eh um anao.
aragorn eh um humano.
legolas eh um elfo.
frodo eh um hobbit.
sam eh um hobbit.
gandalf eh um mago.
galadriel eh uma elfa.
merry eh um hobbit.
pippin eh um hobbit.
boromir eh um humano.
arwen eh uma elfa.
bilbo eh um hobbit.
saruman eh um mago.

:-op(100,xfx,vence).
:-op(60,fx,de).

tesoura vence de papel.
papel vence de pedra.
pedra vence de tesoura.

:-op(100,xfx,salva).

doctor salva galifrey.
doctor salva terra.
doctor salva clara.
clara salva doctor.
tardis salva doctor.

X salva Y :-
    X salva Z,
    Z salva Y.

:-op(100,xfx,�).
:-op(80,fx,ancestral).
:-op(80,fx,pai).
:-op(50,fx,de).

joao � pai de pedro.
pedro � pai de jose.
pedro � pai de ana.
jose � pai de antonio.
lucas � pai de joao.

X � ancestral de Y:-
    X � pai de Y.
X � ancestral de Y:-
    X � pai de Z,
    Z � ancestral de Y.









