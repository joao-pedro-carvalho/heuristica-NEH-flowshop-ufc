import os
import numpy as np
import matplotlib.pyplot as plt
import re # Importando a biblioteca de expressões regulares

def parse_from_file_content(content: str):
    """
    CORRIGIDO: Extrai a matriz de tempos de processamento do conteúdo textual do arquivo,
    usando o formato [PT=...]. Retorna uma matriz no formato (Máquinas x Tarefas).
    """
    pt_match = re.search(r'\[PT=([^\]]+)\]', content)
    if not pt_match:
        raise ValueError("Formato de instância inválido: seção [PT] não encontrada.")

    pt_string = pt_match.group(1).strip()
    
    processing_times = []
    machine_rows = pt_string.split(';')
    for row in machine_rows:
        if row:
            job_times = [int(t) for t in row.split(',')]
            processing_times.append(job_times)
            
    # Retorna a matriz transposta para ficar no formato (Máquinas x Tarefas)
    return np.array(processing_times, dtype=int)

def calculate_makespan(processing_times: np.ndarray, sequence: list) -> int:
    """
    CORRIGIDO: Calcula o makespan para uma sequência de tarefas.
    Assume que processing_times está no formato (Máquinas x Tarefas).
    """
    num_machines, num_jobs_total = processing_times.shape
    num_jobs_in_sequence = len(sequence)
    
    # Matriz para armazenar os tempos de conclusão
    completion_times = np.zeros((num_machines, num_jobs_in_sequence), dtype=int)
    
    # Calcula os tempos para a primeira tarefa da sequência
    first_job_in_seq = sequence[0]
    completion_times[0, 0] = processing_times[0, first_job_in_seq]
    for m in range(1, num_machines):
        completion_times[m, 0] = completion_times[m-1, 0] + processing_times[m, first_job_in_seq]
        
    # Calcula os tempos para as tarefas restantes na sequência
    for j_idx in range(1, num_jobs_in_sequence):
        job = sequence[j_idx]
        # Tempo na primeira máquina
        completion_times[0, j_idx] = completion_times[0, j_idx-1] + processing_times[0, job]
        # Tempos nas máquinas restantes
        for m in range(1, num_machines):
            completion_times[m, j_idx] = max(completion_times[m-1, j_idx], completion_times[m, j_idx-1]) + processing_times[m, job]
            
    return completion_times[-1, -1]

def neh_heuristic(processing_times: np.ndarray):
    """
    CORRIGIDO: Implementa a heurística NEH para minimizar o makespan.
    Assume que processing_times está no formato (Máquinas x Tarefas).
    """
    num_machines, num_jobs = processing_times.shape
    
    # Soma os tempos de processamento por tarefa (somando as colunas)
    job_sums = np.sum(processing_times, axis=0)
    
    # Ordena as tarefas em ordem decrescente da soma
    sorted_jobs_indices = np.argsort(-job_sums)

    best_sequence = []
    for job_idx in sorted_jobs_indices:
        best_temp_sequence = None
        best_temp_makespan = float('inf')
        
        # Tenta inserir a tarefa em todas as posições possíveis
        for i in range(len(best_sequence) + 1):
            trial_sequence = best_sequence[:i] + [job_idx] + best_sequence[i:]
            trial_makespan = calculate_makespan(processing_times, trial_sequence)
            
            if trial_makespan < best_temp_makespan:
                best_temp_makespan = trial_makespan
                best_temp_sequence = trial_sequence
                
        best_sequence = best_temp_sequence
        
    final_makespan = calculate_makespan(processing_times, best_sequence)
    return best_sequence, final_makespan

def plot_gantt_chart(processing_times, sequence, filename):
    """
    CORRIGIDO: Gera um gráfico de Gantt da sequência.
    Assume que processing_times está no formato (Máquinas x Tarefas).
    """
    num_machines, _ = processing_times.shape
    num_jobs_in_seq = len(sequence)

    fig, ax = plt.subplots(figsize=(15, 8))
    colors = plt.cm.get_cmap('tab20', len(sequence))

    completion_times = np.zeros((num_machines, num_jobs_in_seq))
    
    for j_idx, job in enumerate(sequence):
        for m in range(num_machines):
            start_time_on_machine = completion_times[m, j_idx-1] if j_idx > 0 else 0
            start_time_from_prev_machine = completion_times[m-1, j_idx] if m > 0 else 0
            
            start_time = max(start_time_on_machine, start_time_from_prev_machine)
            duration = processing_times[m, job]
            completion_times[m, j_idx] = start_time + duration
            
            ax.barh(f"Máquina {m+1}", duration, left=start_time, color=colors(job), edgecolor='black', label=f"Tarefa {job+1}")
            ax.text(start_time + duration/2, m, f"J{job+1}", ha='center', va='center', color='white', weight='bold')

    ax.set_xlabel("Tempo")
    ax.set_ylabel("Recursos")
    ax.set_title(f"Gráfico de Gantt para a Instância: {filename}")
    ax.grid(axis='x', linestyle='--', alpha=0.6)
    
    # Inverte a ordem das máquinas para M1 ficar no topo
    ax.invert_yaxis()
    plt.tight_layout()
    plt.show()

def main():
    instancias_dir = "instancias"
    if not os.path.isdir(instancias_dir):
        print(f"Erro: Pasta '{instancias_dir}' não encontrada.")
        return

    arquivos = sorted([f for f in os.listdir(instancias_dir) if f.endswith('.txt')])
    if not arquivos:
        print("Nenhuma instância .txt encontrada na pasta 'instancias'.")
        return

    for arquivo in arquivos:
        caminho = os.path.join(instancias_dir, arquivo)
        with open(caminho, 'r') as file:
            content = file.read()

        print("="*60)
        print(f"Processando Arquivo: {arquivo}")
        
        try:
            processing_times = parse_from_file_content(content)
            best_sequence, best_makespan = neh_heuristic(processing_times)
            
            # Adiciona 1 aos índices para exibição (J1, J2, etc.)
            sequence_for_display = [j + 1 for j in best_sequence]
            
            print(f"  Melhor Sequência: {sequence_for_display}")
            print(f"  Makespan Final: {best_makespan}")
            
            plot_gantt_chart(processing_times, best_sequence, arquivo)
            
        except Exception as e:
            print(f"  Erro ao processar {arquivo}: {e}")

if __name__ == "__main__":
    main()
