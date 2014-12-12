import re
import time


class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __neq__(self, other):
        return self.__eq__(other)

    def __str__(self):
        return '(%s, %s)' % (self.x, self.y)

    def __repr__(self):
        return self.__str__()


class Bug(object):
    def __init__(self, id):
        self.id = id
        self.colors = {}
        self.frame = None
        self.position = None
        self.dead = False
        self.finished = False

    def color(self, color):
        self.colors.get('color', 0)

    def set_color(self, color, value):
        self.colors[color] = int(value)

    def set_frame(self, frame):
        self.frame = int(frame)

    def set_position(self, x, y):
        self.position = Position(x, y)

    def check_dead(self):
        dead = True
        for value in self.colors.values():
            if value > 0:
                dead = False
                break
        self.dead = dead

    def __str__(self):
        return '%s - %s - %s' % (self.id, self.colors, self.frame)

    def __repr__(self):
        return self.__str__()


class Tower(object):
    def __init__(self, id):
        self.id = id
        self.colors = {}
        self.position = None

    def set_colors(self, colors_str):
        for color_str in colors_str.split(','):
            name = color_str.split(':')[0]
            val = int(color_str.split(':')[1])
            self.colors[name] = val

    def set_position(self, pos_str):
        x = int(pos_str.split(',')[0])
        y = int(pos_str.split(',')[1])
        self.position = Position(x, y)

    def __str__(self):
        return '%s - %s - %s' % (self.id, self.colors, self.position)

    def __repr__(self):
        return self.__str__()


class Map(object):
    def __init__(self, rows):
        self.rows = rows
        self.start, self.end = self.find_start_end()
        self.bug_road = self.find_bug_road()

    def find_bug_road(self):
        pos = self.start
        road = [pos]
        visited = set([(pos.x, pos.y)])
        while pos != self.end:
            pos = self._next_bug_step(pos, visited)
            visited.add((pos.x, pos.y))
            if not next:
                raise Exception('Something wrong with the bug road')
            road.append(pos)
        return road

    def _next_bug_step(self, pos, visited):
        neighbors = self.get_neighbors(pos)
        for neighbor in neighbors:
            if self.get_pos_value(neighbor.x, neighbor.y) == 'X':
                return neighbor
            if self.get_pos_value(neighbor.x, neighbor.y) == '1' and\
                (neighbor.x, neighbor.y) not in visited:
                    return neighbor
        return None

    def check_tower_pos(self, x, y):
        pos_value = self.get_pos_value(x, y)
        if not pos_value:
            return False
        return True

    def get_pos_value(self, x, y):
        if not self.check_in_map(x, y):
            return None
        return self.rows[y][x]

    def get_neighbors(self, pos):
        neighbors = [(pos.x+1, pos.y), (pos.x-1, pos.y), (pos.x, pos.y+1),
            (pos.x, pos.y-1)]
        return [Position(x, y) for (x, y) in neighbors
            if self.check_in_map(x, y)]

    def check_in_map(self, x, y):
        if y < 0 or y >= self.number_of_rows():
            return False
        if x < 0 or x >= self.number_of_cols():
            return False
        return True

    def find_start_end(self):
        start = None
        end = None
        for y, row in enumerate(self.rows):
            for x, col in enumerate(row):
                if col == 'E':
                    start = Position(x,y)
                elif col == 'X':
                    end = Position(x,y)
        return (start, end)

    def number_of_rows(self):
        return len(self.rows)

    def number_of_cols(self):
        return len(self.rows[0])

    def show(self, bugs, towers):
        bug_positions = {}
        tower_positions = {}

        for bug in bugs:
            if not bug.position:
                continue
            pos_bugs = bug_positions.setdefault(
                (bug.position.x, bug.position.y), [])
            pos_bugs.append(bug)

        for tower in towers:
            if not tower.position:
                continue
            # we will only have one tower per position
            tower_positions[(tower.position.x, tower.position.y)] = tower

        show_rows = []
        max_elem_len = 1
        for y, row in enumerate(self.rows):
            show_row = []
            for x, val in enumerate(row):
                bugs = bug_positions.get((x,y))
                tower = tower_positions.get((x,y))

                if bugs:
                    elem = self.show_bugs(bugs)
                elif tower:
                    elem = tower.id
                else:
                    elem = val
                show_row.append(elem)
                if len(elem) > max_elem_len:
                    max_elem_len = len(elem)
            show_rows.append(show_row)

        # all elements should have the same length
        for y, row in enumerate(show_rows):
            for x, elem in enumerate(row):
                row[x] = elem + (max_elem_len - len(elem)) * ' '

        print('\n'.join(['  '.join(row) for row in show_rows]))

    def show_bugs(self, bugs):
        if len(bugs) == 1:
            return bugs[0].id
        elif len(bugs) > 1:
            return 'B(' + ','.join([bug.id.split('B')[1] for bug in bugs]) + ')'

    def __str__(self):
        return '\n'.join([' '.join(row) for row in self.rows])

    def __repr__(self):
        return self.__str__()


class Action(object):
    NEW_TOWER = 'new_tower'
    SHOOT = 'shoot'

    def __init__(self, action_type, frame, attrs):
        self.action_type = action_type
        self.frame = frame
        self.attrs = attrs

    def __str__(self):
        return '%s - %s - %s' % (self.action_type, self.attrs, self.frame)

    def __repr__(self):
        return self.__str__()


class TDGame(object):
    def __init__(self):
        self.is_initialized = False
        self.settings = False
        self.bugs = None
        self.map = None
        self.life = 0
        self.money = 0

    def initialize(self, f_in, f_actions=None):
        self.settings = self._read_settings(f_in)
        self.bugs = self._read_bugs(f_in)
        self.map = self._read_map(f_in)

        self.life = self._get_setting('starting_life')
        self.money = self._get_setting('starting_money')

        self.actions = []
        if f_actions:
            self.actions = self._read_actions(f_actions)
        self.is_initialized = True
        self.simulation_started = False

    def _get_setting(self, name):
        return self.settings.get(name)

    def start_simulation(self):
        if not self.is_initialized:
            return
        if self.simulation_started:
            return
        self.towers = {}
        self.frame = -1
        self.frames = self._group_by_frame(self.actions)
        self.simulation_started = True
        self.print_state()

    def next_step(self):
        if not self.simulation_started:
            return
        self.frame += 1
        actions = self.frames.get(self.frame)
        print(actions)

        self._build_towers(actions)
        self._move_bugs()
        self._put_bugs_on_map()
        self._shoot(actions)
        # will mark dead bugs
        self._check_dead_bugs()
        # compute damage
        self._compute_damage()
        self._check_life()
        self._give_rewards()
        finished = self._check_game_finished()
        if finished:
            print('The game has finished. You KILLED all the BUGS!')
        self._clear_bugs()

        self.print_state()

    def dump_actions(self, f_solution):
        dump_actions = []
        for action in self.actions:
            rows = [
                'action=%s' % (action.action_type, ),
                'frame=%s' % (action.frame, )
            ]
            rows.extend([
                '%s=%s' % (name, value)
                for name, value in action.attrs.items()
            ])
            dump_action = '\n'.join(rows)
            dump_actions.append(dump_action)    
        f_solution.write('\n\n'.join(dump_actions))
        f_solution.flush()

    def action_new_tower(self, tower_id, position, colors):
        x = position[0]
        y = position[1]
        attrs = {
            'name': tower_id,
            'position': ','.join([str(x),str(y)]),
            'colors': ','.join(['%s:%s' % (name, val)
                                for name, val in colors.items()])
        }
        action = Action(Action.NEW_TOWER, self.frame+1, attrs)
        self._add_action_to_game(action)

    def action_shoot(self, tower_id, bug_id):
        attrs = {'tower_name': tower_id, 'bug_name': bug_id}
        action = Action(Action.SHOOT, self.frame+1, attrs)
        self._add_action_to_game(action)        

    def _add_action_to_game(self, action):
        self.actions.append(action)
        frame_actions = self.frames.setdefault(action.frame, [])
        frame_actions.append(action)

    def _build_towers(self, actions):
        if not actions:
            return
        for action in actions:
            if not action.action_type == Action.NEW_TOWER:
                continue

            # check if id of tower already exists
            tower_id = action.attrs.get('name')
            if tower_id in self.towers:
                print('ERROR: There is already a tower with the same id %s' % (tower_id,))
                return
            # check if the position is valid
            pos = self._parse_tower_postion(action.attrs.get('position'))
            # check position is valid on map
            if not self.map.check_tower_pos(pos.x, pos.y):
                print('ERROR: Can not build a tower on position %s' % (pos,))
                return
            # check that there are no other towers on this position
            if self._is_tower_in_pos(pos.x, pos.y):
                print('ERROR: Tower is already build on position %s' % (pos,))

            # check if we have enough resources
            if self.money < self._get_setting('tower_cost'):
                print('ERROR: not enought resources to build a tower')
                return
            self.money -= self._get_setting('tower_cost')

            tower = Tower(action.attrs.get('name'))
            tower.set_colors(action.attrs.get('colors'))
            tower.set_position(action.attrs.get('position'))
            self.towers[tower.id] = tower

    def _is_tower_in_pos(self, x, y):
        for tower in self.towers.values():
            if tower.position.x == x and tower.position.y == y:
                return True
        return False

    def _parse_tower_postion(self, pos_str):
        x = int(pos_str.split(',')[0])
        y = int(pos_str.split(',')[1])
        return Position(x, y)

    def _move_bugs(self):
        for bug in self.bugs.values():
            if not bug.position:
                continue
            bug.position = self._next_bug_pos(bug)
            # get bug position on bug road
            if self._is_bug_finished(bug):
                bug.finished = True

    def _is_bug_finished(self, bug):
        return bug.position == self.map.end

    def _next_bug_pos(self, bug):
        if not bug.position:
            return None
        try:
            bug_pos_index = self.map.bug_road.index(bug.position)
            if bug_pos_index + 1 >= len(self.map.bug_road):
                return bug.position
            return self.map.bug_road[bug_pos_index+1]
        except ValueError:
            return None 

    def _put_bugs_on_map(self):
        for bug in self.bugs.values():
            if bug.frame == self.frame:
                # the bug will enter the game
                bug.position = self.map.start

    def _shoot(self, actions):
        already_shot = set()
        if not actions:
            return
        for action in actions:
            if not action.action_type == Action.SHOOT:
                continue
            tower_id = action.attrs.get('tower_name')
            bug_id = action.attrs.get('bug_name')
            if tower_id in already_shot:
                print('ERROR: This tower already shot: %s' % (tower_id,))

            tower = self.towers.get(tower_id)
            bug = self.bugs.get(bug_id)

            if not bug or not self._in_range(tower, bug):
                print('ERROR: bug not in range of tower (%s - %s)' % (bug.id, tower.id))

            self._apply_shot(tower, bug)
            already_shot.add(tower_id)

    def _in_range(self, tower, bug):
        tower_range = self.settings.get('tower_range')
        dx = abs(tower.position.x - bug.position.x)
        dy = abs(tower.position.y - bug.position.y)
        return tower_range >= max(dx, dy)

    def _apply_shot(self, tower, bug):
        for color, value in tower.colors.items():
            bug_value = bug.colors.get(color) - value
            bug.colors[color] = bug_value

    def _check_dead_bugs(self):
        for bug in self.bugs.values():
            bug.check_dead()

    def _compute_damage(self):
        damage = 0
        for bug in self.bugs.values():
            damage += self._damage_per_bug(bug)
        self.life -= damage

    def _damage_per_bug(self, bug):
        damage = 0
        # direct damage
        if bug.finished:
            damage += sum(val for val in bug.colors.values() if val > 0)
        # collateral damage
        for color in bug.colors:
            val = bug.colors[color]
            if val < 0:
                damage += -val
                bug.colors[color] = 0
        return damage

    def _check_life(self):
        # if life is <= 0 then the solution is invalid and the games stops
        if self.life <= 0:
            raise Exception('YOU ARE DEAD !!!')

    def _give_rewards(self):
        reward = self.settings.get('reward_per_bug')
        for bug in self.bugs.values():
            if bug.dead:
                self.money += reward

    def _check_game_finished(self):
        for bug in self.bugs.values():
            if not bug.dead:
                return False
        return True

    def _clear_bugs(self):
        # will clear dead bugs or bugs who have finished the race
        del_bugs = []
        for bug_id, bug in self.bugs.items():
            if bug.dead:
                del_bugs.append(bug_id)
        for bug_id in del_bugs:
            self.bugs.pop(bug_id)

    def print_state(self):
        self.map.show(self.bugs.values(), self.towers.values())

        print('Frame: %s' % (self.frame,))
        print('Life: %s' % (self.life,))
        print('Money: %s' % (self.money,))
        print('Tower range: %s' % (self.settings.get('tower_range')))
        print('Tower cost: %s' % (self.settings.get('tower_cost')))
        print('Reward per bug: %s' % (self.settings.get('reward_per_bug')))

        print()

        bugs = [bug for bug in self.bugs.values()]
        bugs.sort(key=lambda bug: bug.frame)
        for bug in bugs:
            print(bug)
        for tower in self.towers.values():
            print(tower)

    def _read_actions(self, f_actions):
        actions = []
        action = self._read_action(f_actions)
        while action:
            actions.append(action)
            action = self._read_action(f_actions)

        return actions

    def _group_by_frame(self, actions):
        frames = {}
        for action in actions:
            frame_actions = frames.get(action.frame)
            if not frame_actions:
                frame_actions = frames[action.frame] = []
            frame_actions.append(action)

        return frames

    def _read_action(self, f_actions):
        type_line = f_actions.readline().strip()
        frame_line = f_actions.readline().strip()
        if (not type_line) or (not frame_line):
            return None

        action_type = type_line.split('=')[1]
        frame = int(frame_line.split('=')[1])
        attrs = {}
        attr_line = f_actions.readline().strip()
        while attr_line:
            name = attr_line.split('=')[0]
            value = attr_line.split('=')[1]
            attrs[name] = value
            attr_line = f_actions.readline().strip()

        return Action(action_type, frame, attrs)

    def _read_map(self, f_in):
        rows = []
        for line in f_in:
            if line:
                rows.append(line.split())
        return Map(rows)

    def _read_bugs(self, f_in):
        bugs = {}
        re_bug = 'B1 red=57 blue=39 frame=0'
        for line in f_in:
            bug = self._read_bug(line)
            if not bug:
                break
            bugs[bug.id] = bug
        return bugs

    def _read_bug(self, line):
        attrs = line.strip().split()
        if not attrs:
            return None
        bug = Bug(attrs[0])
        for attr in attrs[1:]:
            key_val = attr.split('=')
            if key_val[0] == 'frame':
                bug.set_frame(key_val[1])
            else:
                bug.set_color(key_val[0], key_val[1])
        return bug

    def _read_settings(self, f_in):
        settings = {}
        setting_names = '|'.join(
            ['starting_life', 'starting_money', 'tower_range',
            'tower_cost', 'reward_per_bug'])
        re_settings = re.compile('(?P<name>' + setting_names + ')=(?P<value>[0-9]+)')

        line = f_in.readline()
        m = re_settings.match(line)
        while m:
            settings[m.group('name')] = int(m.group('value'))
            line = f_in.readline()
            m = re_settings.match(line)

        return settings


if __name__ == '__main__':
    print("Let's play TD Game")

    # put the input file (in.txt) and the solution file (if any) in the current dir
    f_in = open('03_thePowersThatBe.txt')
    f_actions = open('03_thePowersThatBe_solution_1.txt')
    
    f_solution_out = open('solution_out.txt', 'w')

    game = TDGame()
    # f_actions is optional, use it if you want to test a solution
    game.initialize(f_in, f_actions)
    game.start_simulation()
    
    # go to next frame:
    # game.next_step()

    # add new tower in next frame
    # game.action_new_tower('T3', (0,1), {'red': 1})

    # shoot bug in next frame
    # game.action_shoot('T3', 'B1')

    # at the end of the game you will have the list of actions in game.actions

    import ipdb;ipdb.set_trace()

    # dump actions to file
    game.dump_actions(f_solution_out)
