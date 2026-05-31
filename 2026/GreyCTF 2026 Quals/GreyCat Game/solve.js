(() => {
  intersects = () => false;

  game.gameOver = false;
  game.running = true;
  game.started = true;

  let collected = new Set();

  const loop = async () => {
    for (let i = 0; i < 2000; i++) {
      
      game.score += game.speed * 0.35;
      game.tick++;
      
      if (i % 20 === 0) {
        await reportRunProgress("running");
      }

      if (isFastPhase()) {
        await revealFlagFragment();

        for (const f of game.spectralFragments) {
          collected.add(f.text)    
          console.log([...collected].join(""))
        }
      }
    }
  };

  loop();
})();