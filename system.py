import cvxpy as cp
import numpy as np

class System:
    devices = {}
    sensors = {}
    apps = {}
    resources = ['power_cost', 'comfort', 'security']
    resource_weights = [1, 1, 1]
    time = 0
    rounded_time = 0
    
    def __init__(self, env):
        self.env = env

    # Name = string with device name
    # Obj = object representing interface to device, implements Device class
    def register_device(self, obj):
        self.devices[obj.name] = obj

    # Name = string with sensor name
    # obj = object representing interface to sensor, implements Sensor class
    def register_sensor(self, obj):
        self.sensors[obj.name] = obj

    # Name = string with app name
    # obj = object representing instance of app, implements App class
    def register_app(self, obj):
        self.apps[obj.name] = obj

    # Print current action set
    def show_running_set(self):
        print("Current action set: " + self.action_set + "\n", end=",")

    @staticmethod
    def action_isduplicate(a0, a1):
        seen = set()
        new_l = []
        l = [a0, a1]

        for d in l:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                new_l.append(d)

        return len(new_l) == 1

    # Update action set
    def process(self):
        requested_actions = []
        weights = []
        man_actions = []
        con_action_pairs = []
        dep_action_pairs = []
        alt_actions = []
        for app in self.apps.values():
            requested_actions_, weights_, mandatory_actions_, contradicting_action_pairs_, dependent_action_pairs_, alternative_actions_ =\
                app.update(self)
            
            #Merge action sets
            base_idx = len(requested_actions)
            requested_actions += requested_actions_
            weights += weights_
            alt_actions += alternative_actions_

            man_actions += [x + base_idx for x in mandatory_actions_]
            con_action_pairs += [set([x[0] + base_idx, x[1] + base_idx])
                                 for x in contradicting_action_pairs_]
            dep_action_pairs += [set([x[0] + base_idx, x[1] + base_idx])
                                 for x in dependent_action_pairs_]
            for x in alternative_actions_:
                s = []
                for y in x:
                    s.append(y + base_idx)
                alt_actions.append(set(s))

        # Find duplicate actions
        removed_actions = []
        for i0 in range(len(requested_actions)):
            a0 = requested_actions[i0]
            dups = []
            for i1 in range(i0 + 1, len(requested_actions)):
                a1 = requested_actions[i1]
                if System.action_isduplicate(a0, a1):
                    dups.append(i1)
            
            weights_vec = weights[i0]
            for d in dups:
                # Update weights
                # Choose the action set with the highest weights
                for i in range(len(self.resources)):
                    weights_vec[i] = max(weights_vec[i], weights[d][i])

            # Update weight list
            weights[i0] = weights_vec
            for d in dups:
                weights[d] = weights_vec
                removed_actions.append(d)   # Mark duplicated actions as removed

            # Update conflict indices
            man_actions = [a0 if x in dups else x for x in man_actions]
            con_action_pairs = [set([a0 if y in dups else y for y in x]) for x in con_action_pairs]
            dep_action_pairs = [set([a0 if y in dups else y for y in x]) for x in dep_action_pairs]
            alt_actions = [set([a0 if y in dups else y for y in x]) for x in alt_actions]

        # Remove duplicated actions
        action_cnt = len(requested_actions)
        for d in removed_actions:
            requested_actions[d] = None
            action_cnt -= 1

        # Different actions executing on the same device are exclusive conflicts
        for i0 in range(len(requested_actions)):
            a0 = requested_actions[i0]
            for i1 in range(i0 + 1, len(requested_actions)):
                a1 = requested_actions[i1]
                if a0["device"] == a1["device"]:
                    con_action_pairs.append(set([i0, i1]))

        # Remove duplicate conflicts
        man_actions = list(set(man_actions))
        con_action_pairs = list(set(con_action_pairs))
        dep_action_pairs = list(set(dep_action_pairs))
        alt_actions = list(set(alt_actions))

        # Convert into ILP problem
        mu = cp.Variable(action_cnt, integer=True, boolean=True)  # whether or not the action is to be performed
        
        # Define constraints
        constraints = []
        for m in man_actions:
            constraints.append(mu[m] == 1)
            
        for e in dep_action_pairs:
            e_l = list(e)
            constraints.append(mu[e_l[0]] - mu[e_l[1]] == 0)

        for e in con_action_pairs:
            e_l = list(e)
            constraints.append(mu[e_l[0]] + mu[e_l[1]] <= 1)

        for e in alt_actions:
            e_l = list(e)
            c = mu[e_l[0]] + mu[e_l[1]]
            for idx in range(2, len(e_l)):
                c += mu[e_l[idx]]
            constraints.append(c <= 1)

        # Define cost function
        cost = None
        cost_i = 0
        for j in range(len(self.resource_weights)):
            c = None
            act_idx = 0
            for i in range(len(requested_actions)):
                if requested_actions[i] != None:
                    if c == None:
                        c = mu[act_idx] * weights[act_idx][j]
                    else:
                        c += mu[act_idx] * weights[act_idx][j]
                    act_idx += 1
            if cost_i == 0:
                cost = c * self.resource_weights[j]
                cost_i += 1
            else:
                cost += c * self.resource_weights[j]

        # Run ILP
        problem = cp.Problem(cp.Maximize(cost), constraints)
        problem.solve(solver=cp.ECOS_BB)
        running_actions = np.round(mu.value)

        # Execute actions
        act_cntr = 0
        for act_idx in range(len(running_actions)):
            if requested_actions[act_idx] != None:
                if running_actions[act_cntr] == 1:
                    # submit action
                    pass
                act_cntr += 1

        # Update all devices and sensors
        for dev in self.devices.values():
            dev.update(self, self.env)

        for sense in self.sensors.values():
            sense.update(self, self.env)

        self.time += 1
        self.rounded_time = self.time % (24 * 60 * 60)
