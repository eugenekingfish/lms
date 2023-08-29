class linear_module:
    def __init__(self, head, socle):
        if head < socle:
            raise("ERROR: Not valid module. socle > head")
        self.head = head
        self.socle = socle

    # Checks whether the module is the zero module
    def is_zero(self):
        if self.head == 0 and self.socle == 0:
            return True
        return False
    
    # kernel of two modules
    @staticmethod
    def kernel(mod_a, mod_b):
        a,b = mod_a # we assume that a == b
        c,d = mod_b
        if b == d:
            return [0,0]
        return [max(b,d) - 1, min(b,d)]
