import java.awt.Color;
import java.awt.Component;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import javax.swing.InputMap;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingUtilities;
import javax.swing.Timer;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;
import javax.swing.UIManager.LookAndFeelInfo;

public class SimplePacMan extends JPanel implements ActionListener {
   private static final int tileSize = 24;
   private static final int numTiles = 80;
   private static final int delay = 100;
   private Timer timer;
   private int pacX = 960;
   private int pacY = 960;
   private static final int topbar = 125;
   private int pacVelocityX = 0;
   private int pacVelocityY = 0;
   private int direction = 0;
   private int[][] maze;
   private boolean loser;
   private boolean winner;
   private int score;
   private final int[][] mazedirs = new int[][]{{0, -1}, {0, 1}, {-1, 0}, {1, 0}};
   private static JFrame frame;
   private JTextBasket barbecue2;
   private JTextBasket barbecue;
   private final String flag = "THIS IS NOT HOW YOU ARE SUPPOSED TO DO THE CHALLENGE. YOU CAN IF YOU WANT BUT IT'LL BE EASIER TO JUST CHEAT :) IF YOU DO REVERSE THIS, PLEASE DO A WRITE UP! I'M VERY CURIOUS TO HEAR THE PROCESS";
   protected static final String pacVelocityZ = "6Ach6HiD0JmCc1L+RwxDRzhW3sC1kS6XydgSuWVFpxVXRU8EjfuMxIMoIzMwK/ii";

   private static void runGUI() {
      JFrame.setDefaultLookAndFeelDecorated(true);
      frame = new JFrame("HacMan");
      LookAndFeelInfo[] var0 = UIManager.getInstalledLookAndFeels();
      int var1 = var0.length;

      for(int var2 = 0; var2 < var1; ++var2) {
         LookAndFeelInfo info = var0[var2];
         if ("GTK+".equals(info.getName())) {
            try {
               UIManager.setLookAndFeel(info.getClassName());
            } catch (InstantiationException | IllegalAccessException | UnsupportedLookAndFeelException | ClassNotFoundException var5) {
               var5.printStackTrace();
            }
            break;
         }
      }

      frame.setDefaultCloseOperation(3);
      SimplePacMan viewer = new SimplePacMan();
      frame.add(viewer);
      frame.pack();
      frame.setSize(1920, 2045);
      frame.setVisible(true);
   }

   public static void main(String[] args) {
      SwingUtilities.invokeLater(new Runnable() {
         public void run() {
            SimplePacMan.runGUI();
         }
      });
   }

   public SimplePacMan() {
      this.generateMaze();
      this.setSize(1920, 2045);
      this.setFocusable(true);
      this.addKeyListener(new KeyAdapter() {
         public void keyPressed(KeyEvent e) {
            switch(e.getKeyCode()) {
            case 37:
               SimplePacMan.this.pacVelocityX = -24;
               SimplePacMan.this.pacVelocityY = 0;
               SimplePacMan.this.direction = 2;
               break;
            case 38:
               SimplePacMan.this.pacVelocityX = 0;
               SimplePacMan.this.pacVelocityY = -24;
               SimplePacMan.this.direction = 1;
               break;
            case 39:
               SimplePacMan.this.pacVelocityX = 24;
               SimplePacMan.this.pacVelocityY = 0;
               SimplePacMan.this.direction = 0;
               break;
            case 40:
               SimplePacMan.this.pacVelocityX = 0;
               SimplePacMan.this.pacVelocityY = 24;
               SimplePacMan.this.direction = 3;
            }

         }
      });
      this.barbecue = new JTextBasket();
      this.barbecue.setName("Cowabunga!");
      this.barbecue.setVisible(true);
      this.barbecue.firePropertyChange("delta", 2, 1);
      this.barbecue2 = new JTextBasket();
      this.barbecue2.setInputMap(2, (InputMap)null);
      this.barbecue2.setVisible(false);
      JTextBasket barbecue2 = new JTextBasket();
      barbecue2.setInputMap(2, (InputMap)null);
      barbecue2.setVisible(true);
      this.timer = new Timer(100, this);
      this.timer.start();
   }

   private void generateMaze() {
      this.maze = new int[80][80];
      ArrayList<Point> walls = new ArrayList();
      Random rand = new Random();
      this.barbecue = new JTextBasket();
      this.barbecue.setName("javacode");
      this.barbecue.setEnabled(false);
      this.add(this.barbecue);
      this.maze = this.prims(walls, rand.nextInt(80), rand.nextInt(80), this.maze, rand);
   }

   private int[][] prims(ArrayList<Point> walls, int startX, int startY, int[][] maze, Random rand) {
      maze[startX][startY] = 1;
      walls = this.addWalls(walls, startX, startY);

      while(true) {
         while(walls.size() > 0) {
            int windex = rand.nextInt(walls.size());
            Point randWall = (Point)walls.get(windex);
            Point[] near = this.passage(randWall);
            if (near.length == 1) {
               maze[randWall.x][randWall.y] = 1;
               int newX = randWall.x + near[0].x * -1;
               int newY = randWall.y + near[0].y * -1;
               if (newX < 0 || newX >= 80 || newY < 0 || newY >= 80) {
                  walls.remove(windex);
                  continue;
               }

               maze[newX][newY] = 1;
               this.addWalls(walls, newX, newY);
            }

            walls.remove(windex);
         }

         return maze;
      }
   }

   private Point[] passage(Point wall) {
      return (Point[])Arrays.stream(this.mazedirs).filter((w) -> {
         return w[0] + wall.x >= 0 && w[0] + wall.x < 80 && w[1] + wall.y >= 0 && w[1] + wall.y < 80 && this.maze[w[0] + wall.x][w[1] + wall.y] == 1;
      }).map((w) -> {
         return new Point(w[0], w[1]);
      }).toArray((x$0) -> {
         return new Point[x$0];
      });
   }

   private ArrayList<Point> addWalls(ArrayList<Point> walls, int x, int y) {
      Arrays.stream(this.mazedirs).filter((w) -> {
         return w[0] + x >= 0 && w[0] + x < 80 && w[1] + y >= 0 && w[1] + y < 80 && this.maze[w[0] + x][w[1] + y] == 0;
      }).map((w) -> {
         return new Point(w[0] + x, w[1] + y);
      }).forEach(walls::add);
      return walls;
   }

   public void actionPerformed(ActionEvent e) {
      if (this.score >= 6942069) {
         this.winner = true;
         this.score = 6942069;
      } else {
         int mazeX = (this.pacX + this.pacVelocityX) / 24;
         int mazeY = (this.pacY + this.pacVelocityY) / 24;
         if (mazeX > 0 && mazeX < 80 && mazeY > 0 && mazeY < 80 && this.maze[mazeX][mazeY] != 0) {
            this.pacX += this.pacVelocityX;
            this.pacY += this.pacVelocityY;
            if (this.maze[mazeX][mazeY] == 1) {
               this.maze[mazeX][mazeY] = 2;
               this.score += 10;
               if (this.score == 64000) {
                  this.loser = true;
               }
            }
         }
      }

      this.repaint();
   }

   protected void paintComponent(Graphics g) {
      for(int x = 0; x < 80; ++x) {
         for(int y = 0; y < 80; ++y) {
            if (this.maze[x][y] == 0) {
               g.setColor(Color.BLUE);
               g.fillRect(x * 24, y * 24 + 125, 24, 24);
            } else {
               g.setColor(Color.BLACK);
               g.fillRect(x * 24, y * 24 + 125, 24, 24);
               if (this.maze[x][y] == 1) {
                  g.setColor(Color.CYAN);
                  g.fillOval(x * 24 + 6, y * 24 + 125 + 6, 12, 12);
               }
            }
         }
      }

      g.setColor(Color.YELLOW);
      g.fillArc(this.pacX, this.pacY + 125, 24, 24, 30 + 90 * this.direction, 300);
      g.setColor(Color.WHITE);
      g.fillRect(0, 0, 1920, 100);
      Graphics2D g2 = (Graphics2D)g;
      int fontSize = 50;
      Font f = new Font("Comic Sans MS", 1, fontSize);
      g2.setFont(f);
      g2.setColor(Color.RED);
      g2.drawString("Highscore: 6942069", 20, 100);
      g2.drawString("Your Score: " + this.score, 1320, 100);
      g2.setColor(Color.BLACK);
      g2.drawString("HAC - MAN", 735, 75);
      if (this.loser) {
         g.setColor(Color.RED);
         g.fillRect(480, 480, 980, 980);
         g.setColor(Color.WHITE);
         g.fillRect(490, 490, 960, 960);
         g2.setColor(Color.RED);
         g2.drawString("YOU LOSE!", 520, 580);
         f = new Font("Comic Sans MS", 1, 30);
         g2.setColor(Color.BLACK);
         g2.setFont(f);
         g2.drawString("In order to win, you need to cheat!", 520, 680);
         g2.drawString("The game will now close in 5... good luck!", 520, 780);
         Executors.newSingleThreadScheduledExecutor().schedule(() -> {
            System.exit(0);
         }, 5L, TimeUnit.SECONDS);
      }

      if (this.winner) {
         g.setColor(Color.GREEN);
         g.fillRect(480, 480, 980, 980);
         g.setColor(Color.WHITE);
         g.fillRect(490, 490, 960, 960);
         g2.setColor(Color.RED);
         g2.drawString("YOU WIN!!!", 520, 580);
         f = new Font("Comic Sans MS", 1, 30);
         g2.setColor(Color.BLACK);
         g2.setFont(f);
         this.setName(Integer.toString(this.score));
         this.getComponents()[0].revalidate();
         g2.drawString("Amazing job! Sometimes it's good to cheat..", 520, 680);
         g2.drawString("Or is it? " + ((Component)Arrays.stream(this.getComponents()).filter((w) -> {
            return w.isEnabled();
         }).findFirst().get()).getName(), 520, 780);
      }

      f = new Font("Comic Sans MS", 1, 25);
      g2.setFont(f);
      g2.drawString("Sometimes you need to hack, man!", 660, 100);
   }
}
