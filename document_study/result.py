import multiprocessing
import ifcopenshell.geom
import ifcopenshell
import ifcopenshell.util.shape
import ifcopenshell.util.selector
import numpy as np

ifc_file = ifcopenshell.open('sample.ifc')
print('ifc_file : ', ifc_file)

list_of_target = ifcopenshell.util.selector.filter_elements(ifc_file, "My_Data.cnv_class=target")
print(list_of_target)

# geom 세팅 생성
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)

# Target 객체 반복
for element in list_of_target:
    # shape 가져오기
    shape = ifcopenshell.geom.create_shape(settings, element)
    geometry = shape.geometry
    verts = np.array(geometry.verts).reshape(-1,3)
    
    #중심점 구하기
    center = verts.mean(axis=0)
    print('center : ', center)

    # 소수점반올림
    rounded_center = np.round(center, 3)
    print("Rounded center point:", rounded_center)



    

tree = ifcopenshell.geom.tree()
settings = ifcopenshell.geom.settings()
iterator = ifcopenshell.geom.iterator(settings, ifc_file, multiprocessing.cpu_count())
if iterator.initialize():
    while True:
        # Use triangulation to build a BVH tree
        # tree.add_element(iterator.get())

        # Alternatively, use this code to build an unbalanced binary tree
        tree.add_element(iterator.get_native())

        if not iterator.next():
            break

origin = (0., 0., 0.)
direction = (1., 0., 0.)
results = tree.select_ray(origin, direction, length=50.)
print(results)
import ifcopenshell.util

def swig_point3d_to_tuple(p):
    return tuple(map(float, str(p).strip("()").split(",")))

for result in results:
    print(ifc_file.by_id(result.instance.id()))  # 교차된 IFC 객체

    # ✅ 위치 추출
    intersection_point = swig_point3d_to_tuple(result.position)
    print("Intersection Point:", intersection_point)

    # ✅ 거리
    print("Distance:", result.distance)

    # ✅ 노멀
    normal_vector = swig_point3d_to_tuple(result.normal)
    print("Normal:", normal_vector)

    # ✅ 내적
    print("Dot Product:", result.dot_product)