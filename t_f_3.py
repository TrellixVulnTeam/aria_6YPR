class Solution(object):
    def canPlaceFlowers(self, flowerbed, n):
        if len(flowerbed) == 1 and flowerbed[0] == 0 and n == 1:
            return True
        if n == 0:
            return True
        else:
            for i in range(0, len(flowerbed) - 1):
                if flowerbed[0] == 0 and flowerbed[1] == 0:
                    n = n -1
                    flowerbed[0] = 1
                    if n == 0:
                        return True
                if flowerbed[i] == 0 and flowerbed[i + 1] == 0 and i+1 != len(flowerbed) and flowerbed[i+2] != 1:
                    n = n - 1
                    flowerbed[i + 1] = 1
                    if n == 0:
                        return True
                if flowerbed[-1] == 0 and flowerbed[-2] == 0:
                    n = n - 1
                    flowerbed[-1] = 1
                    if n == 0:
                        return True
            else:
                return False





if __name__ == '__main__':
    r = Solution.canPlaceFlowers(self=int, flowerbed=[0], n=1)
    print(r)