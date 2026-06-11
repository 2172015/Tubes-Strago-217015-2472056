import time
from queue import PriorityQueue

class Node:
    def __init__(self, level, current_cost, current_skill, selected_count, selected_ids, bound):
        self.level = level                  
        self.current_cost = current_cost    
        self.current_skill = current_skill  
        self.selected_count = selected_count
        self.selected_ids = selected_ids    
        self.bound = bound                  

    def __lt__(self, other):
        return self.bound > other.bound

def hitung_bound(node, k, B, n, kandidat):
    if node.current_cost > B or node.selected_count > k:
        return 0
    
    bound_skill = node.current_skill
    current_cost = node.current_cost
    current_count = node.selected_count
    
    j = node.level + 1
    while j < n and current_count < k and current_cost + kandidat[j]['biaya'] <= B:
        bound_skill += kandidat[j]['skill']
        current_cost += kandidat[j]['biaya']
        current_count += 1
        j += 1
        
    if j < n and current_count < k:
        sisa_budget = B - current_cost
        bound_skill += kandidat[j]['skill'] * (sisa_budget / kandidat[j]['biaya'])
        
    return bound_skill

def jalankan_branch_and_bound(k_target, budget, data_kandidat):
    waktu_mulai = time.time()
    kandidat = sorted(data_kandidat, key=lambda x: x['skill']/x['biaya'], reverse=True)
    n = len(kandidat)
    
    pq = PriorityQueue()
    history_langkah = []
    step_counter = 0

    def catat_step(pesan):
        nonlocal step_counter
        step_counter += 1
        history_langkah.append(f"STEP {step_counter}:\n{pesan}")

    akar = Node(-1, 0, 0, 0, [], 0)
    akar.bound = hitung_bound(akar, k_target, budget, n, kandidat)
    pq.put(akar)
    
    catat_step(f"Inisialisasi Node Akar.\nKandidat diurutkan berdasarkan rasio Skill/Biaya.\nHarapan Maksimal Awal (Bound): {akar.bound:.2f}")

    max_skill = 0
    tim_terbaik = []
    jumlah_node = 0
    
    while not pq.empty():
        current = pq.get()
        jumlah_node += 1
        
        info_node = f"Evaluasi Node (Level: {current.level}) | Tim Saat Ini: {current.selected_ids}\nSkill: {current.current_skill} | Biaya: ${current.current_cost} | Bound: {current.bound:.2f}"
        
        if current.bound <= max_skill:
            catat_step(f"{info_node}\n-> DIPANGKAS (Pruning): Nilai bound ({current.bound:.2f}) lebih kecil/sama dengan max skill saat ini ({max_skill}).")
            continue
            
        level = current.level + 1
        if level == n:
            continue
            
        catat_step(f"{info_node}\n-> MENGEMBANGKAN CABANG untuk kandidat berikutnya: {kandidat[level]['id']} (Skill: {kandidat[level]['skill']}, Biaya: ${kandidat[level]['biaya']})")

        # CABANG KIRI (Memilih pemain)
        if current.current_cost + kandidat[level]['biaya'] <= budget and current.selected_count + 1 <= k_target:
            pilih_node = Node(
                level, 
                current.current_cost + kandidat[level]['biaya'], 
                current.current_skill + kandidat[level]['skill'], 
                current.selected_count + 1, 
                current.selected_ids + [kandidat[level]['id']], 
                0
            )
            
            if pilih_node.selected_count == k_target and pilih_node.current_skill > max_skill:
                max_skill = pilih_node.current_skill
                tim_terbaik = pilih_node.selected_ids
                catat_step(f"*** REKOR BARU! ***\nTim penuh terbentuk: {tim_terbaik}\nTotal Skill Max baru: {max_skill}")
                
            pilih_node.bound = hitung_bound(pilih_node, k_target, budget, n, kandidat)
            if pilih_node.bound > max_skill:
                pq.put(pilih_node)
                catat_step(f"   [+] Simpul KIRI dibuat (Pilih {kandidat[level]['id']}). Bound = {pilih_node.bound:.2f}. Masuk ke antrean.")
            else:
                catat_step(f"   [-] Simpul KIRI dibuat (Pilih {kandidat[level]['id']}), TAPI dipangkas karena Bound ({pilih_node.bound:.2f}) <= Max Skill ({max_skill}).")
                
        # CABANG KANAN (Tolak pemain)
        if current.selected_count + (n - 1 - level) >= k_target:
            tolak_node = Node(
                level, 
                current.current_cost, 
                current.current_skill, 
                current.selected_count, 
                current.selected_ids.copy(), 
                0
            )
            tolak_node.bound = hitung_bound(tolak_node, k_target, budget, n, kandidat)
            if tolak_node.bound > max_skill:
                pq.put(tolak_node)
                catat_step(f"   [+] Simpul KANAN dibuat (Tolak {kandidat[level]['id']}). Bound = {tolak_node.bound:.2f}. Masuk ke antrean.")
            else:
                 catat_step(f"   [-] Simpul KANAN dibuat (Tolak {kandidat[level]['id']}), TAPI dipangkas karena Bound ({tolak_node.bound:.2f}) <= Max Skill ({max_skill}).")
                 
    waktu_eksekusi = time.time() - waktu_mulai
    
    catat_step(f"PENCARIAN SELESAI.\nTim Terbaik: {tim_terbaik}\nSkill Maksimal: {max_skill}")
    
    return {
        'tim_terbaik': tim_terbaik,
        'max_skill': max_skill,
        'biaya_terpakai': sum(p['biaya'] for p in kandidat if p['id'] in tim_terbaik),
        'nodes_visited': jumlah_node,
        'waktu_eksekusi': waktu_eksekusi,
        'langkah_langkah': history_langkah
    }