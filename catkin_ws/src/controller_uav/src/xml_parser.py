import xml.etree.ElementTree as ET
from collections import defaultdict


def parser_world(filename):
	tree = ET.parse(filename)
	objects = ['ground_plane']
	root = tree.getroot()
	print(root)
	print('Tag',root.tag)
	print('Attributes',root.attrib)

	for child in root:
		root2 = child

	count=0
	for child in root2:
		count +=1
		#print('Child count',count)
		#print('Child Tag', child.tag)
		#print('Child Attributes', child.attrib)

	dict_obj = defaultdict(list)

	for model in root2.findall('model'):
		name = model.get('name')
		print(name)
		if(name not in objects):
			#print('HERE')
			pose = (model.find('pose').text).split(' ')
			for val in pose:
				dict_obj[name].append(float(val))
			#print(dict_obj[name])
				

	return dict_obj

if __name__ == '__main__':
	
	objects = parser_world('my_world_2.world')
	print('Objects:', objects)
		






