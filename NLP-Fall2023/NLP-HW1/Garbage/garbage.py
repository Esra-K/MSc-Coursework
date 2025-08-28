

def get_text_positions(text, x_data, y_data, txt_width, txt_height):
    a = zip(y_data, x_data)
    text_positions = list(y_data)
    for index, (y, x) in enumerate(a):
        local_text_positions = [i for i in a if i[0] > (y - txt_height)
                            and (abs(i[1] - x) < txt_width * 2) and i != (y,x)]
        if local_text_positions:
            sorted_ltp = sorted(local_text_positions)
            if abs(sorted_ltp[0][0] - y) < txt_height: #True == collision
                differ = np.diff(sorted_ltp, axis=0)
                a[index] = (sorted_ltp[-1][0] + txt_height, a[index][1])
                text_positions[index] = sorted_ltp[-1][0] + txt_height*1.01
                for k, (j, m) in enumerate(differ):
                    #j is the vertical distance between words
                    if j > txt_height * 2: #if True then room to fit a word in
                        a[index] = (sorted_ltp[k][0] + txt_height, a[index][1])
                        text_positions[index] = sorted_ltp[k][0] + txt_height
                        break
    return text_positions

def text_plotter(text, x_data, y_data, text_positions, txt_width,txt_height):
    for z,x,y,t in zip(text, x_data, y_data, text_positions):
        plt.annotate(str(z), xy=(x-txt_width/2, t), size=12)
        if y != t:
            plt.arrow(x, t,0,y-t, color='red',alpha=0.3, width=txt_width*0.1,
                head_width=txt_width, head_length=txt_height*0.5,
                zorder=0,length_includes_head=True)


# txt_height = 0.0037*(plt.ylim()[1] - plt.ylim()[0])
# txt_width = 0.018*(plt.xlim()[1] - plt.xlim()[0])
#
# text_positions = get_text_positions(list(indices.values()), t[0], t[1], txt_width, txt_height)
#
# text_plotter(list(indices.values()), t[0], t[1], text_positions, txt_width, txt_height)
for i, txt in indices.items():
    plt.annotate(txt, (t[0][i], t[1][i]))
# texts = []
# for x, y, s in zip(t[0], t[1], list(indices.values())):
#     texts.append(plt.text(x, y, s))


# color_map = {"wei": "yellow", "wu":"blue", "shu":"green"}
for i, name in enumerate(names):
    indices[i] = name
    vecs[i] = w2v.wv[name]
    # max_color = 0
    # color = "red"
    # for kingdom in color_map.keys():
    #     score = w2v.wv.similarity(name, kingdom)
    #     if score > max_color:
    #         max_color = score
    #         color = color_map[kingdom]
    # colors.append(color)
    # print(name, vecs[i])
print(len(indices.keys()))

# character_words = []
# for j in range(len(feature_words)):
#     if feature_words[j] in names:
#         character_words.append(j)
#
# min_intercharacter_degree = 10


# if character_words[character_cursor] == j:
#     print("here!")
#     intercharacter_degree += 1
#     character_cursor += 1
#     if intercharacter_degree == min_intercharacter_degree:
#         print("there!")
#         names_indices_to_keep.append(i)

import hunspell
# hobj = hunspell.HunSpell("../Data/en_US.dic", "../Data/en_US.aff")
