# The Crazy Cat Lady Game (Board Game) Simulation

The Crazy Cat Lady Game (Accoutrements LLC, 2013) is a basic spin-and-move board game that follows the life of a feline enthusiast as she visits the park, vet, animal shelter, etc., gaining and losing cats along the way. After playing the game with friends, I used Monte Carlo simulation see if our experiences (landing on the same spaces frequently, difficult to finish, etc.) were typical. I also wanted to simulate application of some "house rules" to speed up the game.

[View the game on Amazon here](https://www.amazon.com/Accoutrements-11893-Crazy-Lady-Game/dp/B001J7AIAU)

[Simulation results visualized (Tableau Public)](https://public.tableau.com/app/profile/klg27/viz/BoardGameSimulationHoldontoYourCats/Dashboard)

#### General assumptions:
* Fair spinner (equal probability of landing on 1-6)
* Spins are independent (the result of spin #2 does not differ based on the landing place of the previous spin)
* The four Wildcat cards are chosen independently with equal probability. The particular set that we played (owned by our friends) contained two of the same card (3 distinct messages).
* Wildcat cards are replaced after each use and re-selected independently, i.e. each time a player lands on a Wildcat space, one of four cards is selected at random. Previous selections do not impact the probability of pulling a card (assumes cards are shuffled each time, and not taken from an ordered stack).
* Space 38 (Animal Control confiscates half your cats): assumes rounding down when a player has an odd number of cats. For example, if a player has 11 cats, five would be sent to the shelter tray.
* The game ends when the first player lands on Home (does not have to land exactly on Home), and the winner is the person with the most cats (not necessarily the person who ended the game). The instructions do not specify a tie-breaker, so I assumed that games could end in a tie.

#### This is a basic spin-and-move game, with very little decision making. However, when decisions were required they were assumed as follows:
* When given the choice to *take from* another player, the player with the *most* cats is chosen (this can be changed to random using the choose_highest variable to False)
* When given the choice to *give to* another player, the player with the *fewest* cats is chosen (this can be changed to random using the choose_highest variable to False)

#### Tray runout
In most cases, players draw cats from the main game tray and lose cats to the animal shelter. In some cases, the game tray may run out of cats, and the game instructions do not specify what to do in that situation. For the base rules, I assumed that *both trays were allowed to run out of cats*, and a players would draw zero cats until the tray was replenished. For example, if a player was instructed to draw two cats from the tray, but the tray was empty, the player would receive no cats on that turn.

This assumption can be changed by setting the allow_tray_runout and/or allow_shelter_runout variables to False (this would assume players use paper clips, coins, pen and paper, etc. to keep track of the cats received when there are no more game pieces available).

While trays can be modeled with no runout, there is no option to model players with no runout.
