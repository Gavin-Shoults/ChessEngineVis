import pygame, sys, chess, chess.engine, matplotlib, os, re, pylab
import matplotlib.pyplot as plt
import numpy as np
from pygame.locals import *
matplotlib.use('Agg')
import matplotlib.backends.backend_agg as agg
directory = os.getcwd()


# setting the FPS
def main():
	clock = pygame.time.Clock()
	pygame.init()
# Setting up the board size/colors
	playerBlack = (70,24,1)
	playerWhite = (255,255,240)
	boardTall = 1000
	boardWide = boardTall * 1.5
	squaresize = int(boardTall / 8)

	engine = chess.engine.SimpleEngine.popen_uci(f"{directory}/Engine/stockfish_15_win_x64_avx2/stockfish_15_x64_avx2.exe")


	#reference for when a square is empty or occupied
	rows = '12345678'
	files = 'abcdefgh'
	board_dict = {}
	for row in rows:
		for file in files:
			board_dict[file+row] = 'Empty'

	

	#png loading module
	def load_png(name):
		fullname = os.path.join(f'{directory}/Assets', name)
		image = pygame.image.load(fullname)
		if image.get_alpha is None:
			image = image.convert()
		return image, image.get_rect()

	#takes position (0,0 top left) and turns into square location
	def getrow(pos):
		rowpos = pos[1]

		if rowpos <= squaresize:
			square_row = '8'
		elif squaresize < rowpos <= squaresize * 2:
			square_row = '7'
		elif squaresize * 2 < rowpos <= squaresize * 3:
			square_row = '6'
		elif squaresize * 3 < rowpos <= squaresize * 4:
			square_row = '5'
		elif squaresize * 4 < rowpos <= squaresize * 5:
			square_row = '4'
		elif squaresize * 5 < rowpos <= squaresize * 6:
			square_row = '3'
		elif squaresize * 6 < rowpos <= squaresize * 7:
			square_row = '2'
		elif squaresize * 7 < rowpos <= squaresize * 8:
			square_row = '1'

	def getfile(pos):
		filepos = pos[0]
		
		if filepos <= squaresize:
			square_file = 'a'
		elif squaresize < filepos <= squaresize * 2:
			square_file = 'b'
		elif squaresize * 2 < filepos <= squaresize * 3:
			square_file = 'c'
		elif squaresize * 3 < filepos <= squaresize * 4:
			square_file = 'd'
		elif squaresize * 4 < filepos <= squaresize * 5:
			square_file = 'e'
		elif squaresize * 5 < filepos <= squaresize * 6:
			square_file = 'f'
		elif squaresize * 6 < filepos <= squaresize * 7:
			square_file = 'g'
		elif squaresize * 7 < filepos <= squaresize * 8:
			square_file = 'h'
		return square_file

	def getsquare(pos):
		posx = pos[0]
		posy = pos[1]
		square_file = 'Z'
		square_row = '0'
		#Getting file (letter)
		if posx <= squaresize:
			square_file = 'a'
		elif squaresize < posx <= squaresize * 2:
			square_file = 'b'
		elif squaresize * 2 < posx <= squaresize * 3:
			square_file = 'c'
		elif squaresize * 3 < posx <= squaresize * 4:
			square_file = 'd'
		elif squaresize * 4 < posx <= squaresize * 5:
			square_file = 'e'
		elif squaresize * 5 < posx <= squaresize * 6:
			square_file = 'f'
		elif squaresize * 6 < posx <= squaresize * 7:
			square_file = 'g'
		elif squaresize * 7 < posx <= squaresize * 8:
			square_file = 'h'
		else:
			return "Outside Game Area"
		#Getting row(number)
		if posy <= squaresize:
			square_row = '8'
		elif squaresize < posy <= squaresize * 2:
			square_row = '7'
		elif squaresize * 2 < posy <= squaresize * 3:
			square_row = '6'
		elif squaresize * 3 < posy <= squaresize * 4:
			square_row = '5'
		elif squaresize * 4 < posy <= squaresize * 5:
			square_row = '4'
		elif squaresize * 5 < posy <= squaresize * 6:
			square_row = '3'
		elif squaresize * 6 < posy <= squaresize * 7:
			square_row = '2'
		elif squaresize * 7 < posy <= squaresize * 8:
			square_row = '1'

		#return square information
		return square_file + square_row



	#opposite of above; take in square and return coords of center)
	def squarecenter(squarepos):
		squarefilein = squarepos[0]
		squarerowin = squarepos[1]
		x_center = '0'
		y_center = '0'

		if squarefilein == 'a':
			x_center = squaresize/2
		elif squarefilein == 'b':
			x_center = squaresize/2 + squaresize
		elif squarefilein == 'c':
			x_center = squaresize/2 + (squaresize * 2)
		elif squarefilein == 'd':
			x_center = squaresize/2 + (squaresize * 3)
		elif squarefilein == 'e':
			x_center = squaresize/2 + (squaresize * 4)
		elif squarefilein =='f':
			x_center = squaresize/2 + (squaresize * 5)
		elif squarefilein == 'g':
			x_center = squaresize/2 + (squaresize * 6)
		elif squarefilein == 'h':
			x_center = squaresize/2 + (squaresize * 7)
			######
		if squarerowin == '8':
			y_center = squaresize/2
		elif squarerowin == '7':
			y_center = squaresize/2 + squaresize
		elif squarerowin == '6':
			y_center = squaresize/2 + (squaresize * 2)
		elif squarerowin == '5':
			y_center = squaresize/2 + (squaresize * 3)
		elif squarerowin == '4':
			y_center = squaresize/2 + (squaresize * 4)
		elif squarerowin == '3':
			y_center = squaresize/2 + (squaresize * 5)
		elif squarerowin == '2':
			y_center = squaresize/2 + (squaresize * 6)
		elif squarerowin == '1':
			y_center = squaresize/2 + (squaresize * 7)

		return (x_center,y_center)


	def getsquarecoords(squarename):
		squarefilein = squarename[0]
		squarerowin = squarename[1]
		x_coord = '0'
		y_coord = '0'

		if squarefilein == 'a':
			x_coord = 0
		elif squarefilein == 'b':
			x_coord = squaresize
		elif squarefilein == 'c':
			x_coord = (squaresize * 2)
		elif squarefilein == 'd':
			x_coord = (squaresize * 3)
		elif squarefilein == 'e':
			x_coord = (squaresize * 4)
		elif squarefilein =='f':
			x_coord = (squaresize * 5)
		elif squarefilein == 'g':
			x_coord = (squaresize * 6)
		elif squarefilein == 'h':
			x_coord = (squaresize * 7)
			######
		if squarerowin == '8':
			y_coord = 0
		elif squarerowin == '7':
			y_coord =  squaresize
		elif squarerowin == '6':
			y_coord = (squaresize * 2)
		elif squarerowin == '5':
			y_coord = (squaresize * 3)
		elif squarerowin == '4':
			y_coord = (squaresize * 4)
		elif squarerowin == '3':
			y_coord = (squaresize * 5)
		elif squarerowin == '2':
			y_coord = (squaresize * 6)
		elif squarerowin == '1':
			y_coord = (squaresize * 7)
		return(x_coord, y_coord)

# pygame initializing
	screen = pygame.display.set_mode((boardWide,boardTall))
	pygame.display.set_caption("Chess")
	pygame.mouse.set_visible(True)
	holding_piece = False
	pickup_square = '00'
	activepiece = []

# drawing the board
	playboard = pygame.Surface(screen.get_size())
	playboard.fill(playerBlack)
	

#setting board with chess module
	logic_board = chess.Board()
	current_team = (bool(logic_board.turn))

	def current_team_color(inputteam=bool):
		if inputteam == False:
			return 'Black'
		else:
			return 'White'



	class GamePiece(pygame.sprite.Sprite):
		def __init__(self,piecepos,team):
			pygame.sprite.Sprite.__init__(self)
			self.team = team
			self.piecepos = piecepos
			self.piecesquare = getsquare(self.piecepos)
			activepiece.append(self)
			pygame.sprite.Group.add(self)
			board_dict[self.piecesquare] = self
		def update(self):
			self.piecesquare = getsquare(self.piecepos)
			self.rect.center = self.piecepos

	class Knight(GamePiece):
		def __init__(self,piecepos,team):
			super().__init__(piecepos,team)
			self.image, self.rect = load_png(f'knight_{team}.png')

	class Rook(GamePiece):
		def __init__(self,piecepos,team):
			super().__init__(piecepos,team)
			self.image, self.rect = load_png(f'rook_{team}.png')

	class Bishop(GamePiece):
		def __init__(self,piecepos,team):
			super().__init__(piecepos,team)
			self.image, self.rect = load_png(f'bishop_{team}.png')

	class Queen(GamePiece):
		def __init__(self,piecepos,team):
			super().__init__(piecepos,team)
			self.image, self.rect = load_png(f'queen_{team}.png')

	class King(GamePiece):
		def __init__(self,piecepos,team):
			super().__init__(piecepos,team)
			self.image, self.rect = load_png(f'king_{team}.png')

	class Pawn(GamePiece):
		def __init__(self,piecepos,team):
			super().__init__(piecepos,team)
			self.image, self.rect = load_png(f'pawn_{team}.png')
		def promote_queen(self):
			self.image, self.rect = load_png(f'queen_{self.team}.png')
		def promote_knight(self):
			self.image, self.rect = load_png(f'knight_{self.team}.png')
		def promote_rook(self):
			self.image, self.rect = load_png(f'rook_{self.team}.png')
		def promote_bishop(self):
			self.image, self.rect = load_png(f'bishop_{self.team}.png')

			#easy function to highligh squares- red if attack, green if move
	def highlight_square(squareinput):
		square = squareinput[0:2]
		active_rect = pygame.Surface((squaresize,squaresize))
		active_rect.set_alpha(100)
		if board_dict[square] != 'Empty':
			active_rect.fill('red')
		else:
			active_rect.fill('#90ee90')
		playboard.blit(active_rect, getsquarecoords(square))

	def is_promotion(piece,targetsquare):
		if type(piece) == Pawn:
			if piece.team == 'white' and targetsquare[1] == '8':
				return True
			elif piece.team == 'black' and targetsquare[1] == '1':
				return True
			else:
				return False
		else:
			return False

	def get_rel_square(inputsquarename):
		rel_y = int(inputsquarename[1])
		x_name = inputsquarename[0]
		rel_x = files.index(x_name) + 1
		return rel_x, rel_y


	def find_best():
		result = engine.play(logic_board, chess.engine.Limit(time=1))
		return result.move



		#there has to be abetter way to get num value of a position...
	def strength_of():
		print('*****')
		move_strengths = []
		for ind_move in logic_board.legal_moves:
			board = logic_board
			board.push(ind_move)
			info = engine.analyse(board,chess.engine.Limit(time = 0.1))
			cp_score = re.findall('\(.*?\)',str(info['score']))[0]
			num_score = cp_score[4:-1]
			if num_score.startswith('e'):
				move_strengths.append((get_rel_square(board.uci(ind_move)[2:4]), -9999))
				board.pop()
				continue
			move_strengths.append((get_rel_square(board.uci(ind_move)[2:4]), int(num_score)))
			board.pop()
		return(move_strengths)

	def heatmap(inputdata):
		rows,cols = (8,8)
		data = np.array([[0 for i in range(cols)] for j in range(rows)], dtype = np.double)
		for value in inputdata:
			squarelocation = value[0]
			squarevalue = value[1]
			squareloc_x = squarelocation[0] - 1
			squareloc_y = 7-(squarelocation[1] - 1)
			data[squareloc_y][squareloc_x] += squarevalue
		data[ data == 0] = np.nan

		#set buffer image with pylab, create matplotlib analysis

		fig = pylab.figure(figsize = [5,5], dpi = 98)
		heatimage = plt.imshow(data,cmap = 'RdBu_r')
		heatimage.axes.xaxis.set_visible(False)
		heatimage.axes.yaxis.set_visible(False)
		plt.title('Strength of Possible Computer Moves')
		colbar = plt.colorbar()
		colbar.set_ticks([])

		#change matplotlib image to string

		canvas = agg.FigureCanvasAgg(fig)
		canvas.draw()
		renderer = canvas.get_renderer()
		raw_data = renderer.tostring_rgb()
		heatsize = canvas.get_width_height()

		#change image string to pygame surface

		heatsurf = pygame.image.fromstring(raw_data,heatsize,'RGB')
		playboard.blit(heatsurf, ((squaresize * 8) + 5,(squaresize * 4) + 5))
		pygame.display.flip()
		

	playboard.fill((200,143,85),(boardTall,0,boardWide-boardTall,boardTall))
	current_color = True
	def draw_board():
		current_draw_color = True
		for i in range(0,8):
			current_draw_color = not current_draw_color
			for j in range (0,8):
				if not current_draw_color:
					playboard.fill(playerWhite,((i*squaresize,j*squaresize),(squaresize,squaresize)))
					current_draw_color = not current_draw_color
				else:
					playboard.fill(playerBlack,((i*squaresize,j*squaresize),(squaresize,squaresize)))
					current_draw_color = not current_draw_color
		




	draw_board()

	font = pygame.font.Font(None, 64)
	text = font.render("White to move", True, (0,0,0))
	textpos = text.get_rect(midtop = (boardWide - (squaresize * 2), 20))
	playboard.blit(text,textpos)
	
	
	
	screen.blit(playboard,(0,0))
	pygame.display.flip()
	
	held_piece = None

	##initialize all the sprites of default pieces in default positions
	#black pieces

	knight_black_one = Knight(squarecenter('b8'),'black')

	knight_black_two = Knight(squarecenter('g8'),'black')
		
	rook_black_one = Rook(squarecenter('a8'),'black')
	
	rook_black_two = Rook(squarecenter('h8'),'black')
	
	bishop_black_one = Bishop(squarecenter('c8'),'black')
	
	bishop_black_two = Bishop(squarecenter('f8'),'black')
	
	king_black = King(squarecenter('e8'),'black')

	queen_black = Queen(squarecenter('d8'),'black')
	

	#pawns,black ... has to be a better way to do this haha

	pawn_black_one = Pawn(squarecenter('a7'),'black')

	pawn_black_two = Pawn(squarecenter('b7'),'black')
	
	pawn_black_three = Pawn(squarecenter('c7'),'black')
	
	pawn_black_four = Pawn(squarecenter('d7'),'black')
	
	pawn_black_five = Pawn(squarecenter('e7'),'black')
	
	pawn_black_six = Pawn(squarecenter('f7'),'black')
	
	pawn_black_seven = Pawn(squarecenter('g7'),'black')
	
	pawn_black_eight = Pawn(squarecenter('h7'),'black')
	

	#white pieces

	knight_white_one = Knight(squarecenter('b1'),'white')
	
	knight_white_two = Knight(squarecenter('g1'),'white')
	
	rook_white_one = Rook(squarecenter('a1'),'white')

	rook_white_two = Rook(squarecenter('h1'),'white')

	bishop_white_one = Bishop(squarecenter('c1'),'white')

	bishop_white_two = Bishop(squarecenter('f1'),'white')

	king_white = King(squarecenter('e1'),'white')

	queen_white = Queen(squarecenter('d1'),'white')
	

	#pawns, white

	pawn_white_one = Pawn(squarecenter('a2'),'white')
	
	pawn_white_two = Pawn(squarecenter('b2'),'white')
	
	pawn_white_three = Pawn(squarecenter('c2'),'white')
	
	pawn_white_four = Pawn(squarecenter('d2'),'white')
	
	pawn_white_five = Pawn(squarecenter('e2'),'white')
	
	pawn_white_six = Pawn(squarecenter('f2'),'white')
	
	pawn_white_seven = Pawn(squarecenter('g2'),'white')
	
	pawn_white_eight = Pawn(squarecenter('h2'),'white')
	
	piecesprites = pygame.sprite.RenderPlain(activepiece)

	while True:
		clock.tick(60)

		#Dealing with player moves
		if current_team_color(current_team) =='White':
			for event in pygame.event.get():

				if event.type == QUIT:
					engine.quit()
					pygame.quit()
					return
				#What to do when picking up a piece
				elif event.type == MOUSEBUTTONDOWN and event.button == 1:
					legal_from_square = []
					draw_board()
				
					#most of the logic is with putting down the piece...
					pickup_square = getsquare(event.pos)
					if pickup_square != "Outside Game Area":
						if board_dict[pickup_square] != 'Empty':
								for pot_move in logic_board.legal_moves:
									if str(pot_move).startswith(pickup_square):
										legal_from_square = str(pot_move)[2:]
										highlight_square(legal_from_square)
								held_piece = board_dict[pickup_square]
								holding_piece = True

				elif event.type == MOUSEBUTTONUP and event.button == 1:
					drop_square = getsquare(event.pos)
					if pickup_square not in board_dict or drop_square not in board_dict:
						if holding_piece:
							held_piece.piecepos = squarecenter(pickup_square)
						pass
					else:
						if drop_square != pickup_square:
							current_move_uci = f'{pickup_square}{drop_square}'

							if is_promotion(held_piece,drop_square):

								current_move_uci += 'q'
								held_piece.promote_queen()
								held_piece.__class__ = Queen

							current_move = chess.Move.from_uci(current_move_uci)

							if current_move in logic_board.legal_moves and holding_piece == True:
								draw_board()
							
								logic_board.push(current_move)
								if board_dict[drop_square] != 'Empty':
									activepiece.remove(board_dict[drop_square])
									pygame.sprite.Group.remove(board_dict[drop_square])
									board_dict[pickup_square] = 'Empty'
									board_dict[drop_square] = held_piece
									held_piece.piecepos = squarecenter(drop_square)
								

								##Kinda awkard logic for dealing with sprites for castle...
								elif type(held_piece) == King and pickup_square.startswith('e'):
									board_dict[pickup_square] = 'Empty'
									board_dict[drop_square] = held_piece
									held_piece.piecepos = squarecenter(drop_square)
									if drop_square.startswith('c'):
										
										board_dict[f'd{drop_square[1]}'] = board_dict[f'a{drop_square[1]}']
										board_dict[f'a{drop_square[1]}'] = 'Empty'
										board_dict[f'd{drop_square[1]}'].piecepos = squarecenter(f'd{drop_square[1]}')
									elif drop_square.startswith('g'):
										
										board_dict[f'f{drop_square[1]}'] = board_dict[f'h{drop_square[1]}']
										board_dict[f'h{drop_square[1]}'] = 'Empty'
										board_dict[f'f{drop_square[1]}'].piecepos = squarecenter(f'f{drop_square[1]}')
								#### ^Castle^

								###En passant
								elif type(held_piece) == Pawn and board_dict[drop_square] == 'Empty':
									if pickup_square[0] != drop_square[0] and pickup_square[1] != drop_square[1]:
								

										passant_square = (drop_square[0] + pickup_square[1])
									

										piecesprites.clear(screen,playboard)
										activepiece.remove(board_dict[passant_square])
										piecesprites = pygame.sprite.Group(activepiece)
										pygame.sprite.Group.remove(board_dict[passant_square])
										piecesprites.draw(screen)
					
										board_dict[passant_square] = 'Empty'
										board_dict[pickup_square] = 'Empty'
										board_dict[drop_square] = held_piece

										held_piece.piecepos = squarecenter(drop_square)

									else:
										board_dict[pickup_square] = 'Empty'
										board_dict[drop_square] = held_piece
										held_piece.piecepos = squarecenter(drop_square)
								### En passant^^^

								else:
									board_dict[pickup_square] = 'Empty'
									board_dict[drop_square] = held_piece
									held_piece.piecepos = squarecenter(drop_square)
								held_piece.update()
								current_team = not current_team		
							else:
								if holding_piece:
									held_piece.piecepos = squarecenter(pickup_square)
								pass
						else:
							if holding_piece:
								held_piece.piecepos = squarecenter(pickup_square)

					##per event updates
				
					held_piece = None
					holding_piece = False
					drop_square = None
					pickup_square = None
					passant_square = None
					piecesprites = pygame.sprite.Group(activepiece)
					

					
						
				
		#dealing with ai moves.
		else:
			draw_board()
			
			#generate a parse-able list from legal moves and return random (temporary)
			
			heatmap(strength_of())

			ai_move = find_best()
			

			#seperate into from and to square, push move
			ai_fromsquare = str(ai_move)[:2]
			ai_tosquare = str(ai_move)[2:4]
			logic_board.push(ai_move)

			#update board dictionary, sprite position of moved piece

			ai_held_piece = board_dict[ai_fromsquare]

			#AI Passant
			if type(ai_held_piece) == Pawn and board_dict[ai_tosquare] == 'Empty':
				if ai_fromsquare[0] != ai_tosquare[0] and ai_fromsquare[1] != ai_tosquare[1]:

					ai_passant_square = (ai_tosquare[0] + ai_fromsquare[1])
				

					piecesprites.clear(screen,playboard)
					activepiece.remove(board_dict[ai_passant_square])
					piecesprites = pygame.sprite.Group(activepiece)
					pygame.sprite.Group.remove(board_dict[ai_passant_square])
					piecesprites.draw(screen)

					board_dict[ai_passant_square] = 'Empty'
					board_dict[ai_fromsquare] = 'Empty'

				else:
					board_dict[ai_fromsquare] = 'Empty'
					ai_held_piece.piecepos = squarecenter(ai_tosquare)
			else:
				board_dict[ai_fromsquare] = 'Empty'
			##^^AI Passant


			##AI Castle

			##^^AI Castle

			#dealing with sprite if any are captured
			piecesprites.clear(screen,playboard)
			if board_dict[ai_tosquare] != 'Empty':
				activepiece.remove(board_dict[ai_tosquare])
			piecesprites = pygame.sprite.Group(activepiece)
			piecesprites.draw(screen)
			

			board_dict[ai_tosquare] = ai_held_piece
			
			ai_held_piece.piecepos = squarecenter(ai_tosquare)
			piecesprites = pygame.sprite.Group(activepiece)
			
			#set move back to player
			current_team = not current_team

		##per-frame updates
		if current_team_color(current_team) == 'White':
			playboard.fill((200,143,85),textpos)
			text = font.render(f"White to Move", True, (0,0,0))
			textpos = text.get_rect(midtop = (boardWide - (squaresize * 2), 20))
			playboard.blit(text,textpos)

		if current_team_color(current_team) == 'Black':
			playboard.fill((200,143,85),textpos)
			text = font.render(f" Black is Thinking", True, (0,0,0))
			textpos = text.get_rect(midtop = (boardWide - (squaresize * 2), 20))
			playboard.blit(text,textpos)



		if logic_board.is_checkmate():
			playboard.fill((200,143,85),textpos)
			text = font.render(f"{current_team_color(not current_team)} wins!", True, (0,0,0))
			playboard.blit(text,textpos)

		if holding_piece:
			held_piece.piecepos = pygame.mouse.get_pos()

		screen.blit(playboard,(0,0))
		piecesprites.clear(screen,playboard)
		piecesprites.draw(screen)
		piecesprites.update()
		pygame.display.flip()
main()