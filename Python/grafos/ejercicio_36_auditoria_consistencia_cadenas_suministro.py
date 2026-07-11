"""Ejercicio 36: Auditoría de Consistencia en Cadenas de Suministro

En una red de suministro multinivel legal, los nodos se clasifican en: Proveedores, Intermedios 
y Consumidores. Un error de diseño ocurre si un Proveedor tiene conexiones de entrada, o si un 
Consumidor tiene conexiones de salida.

    - Implementa un auditor de red que reciba el grafo y tres listas de etiquetas ( proveedores,
    intermedios, Consumidores). El script debe verificar si la estructura del grado viola las 
    reglas de negocio de IO mencionadas y retornar una lista detallada de las violaciones encontradas. 
"""

class SupplyChainAuditor:
    def __init__(self):
        """
        Inicializa el auditor de cadenas de suministro.
        """
        self.graph = {}
        self.proveedores = set()
        self.intermedios = set()
        self.consumidores = set()
        self.violations = []
    
    def load_network(self, graph, proveedores, intermedios, consumidores):
        """
        Carga la red y las clasificaciones de nodos para auditoría.
        
        Args:
            graph: Diccionario con formato {nodo: [lista_de_vecinos_salida]}
            proveedores: Lista de nodos clasificados como proveedores
            intermedios: Lista de nodos clasificados como intermedios
            consumidores: Lista de nodos clasificados como consumidores
        """
        self.graph = graph
        self.proveedores = set(proveedores)
        self.intermedios = set(intermedios)
        self.consumidores = set(consumidores)
        self.violations = []
        
        # Validar que todos los nodos en el grafo estén clasificados
        self._validate_classification_completeness()
        
        # Validar que no haya superposición en las clasificaciones
        self._validate_classification_overlap()
    
    def _validate_classification_completeness(self):
        """
        Verifica que todos los nodos del grafo estén clasificados en alguna categoría.
        """
        all_graph_nodes = set(self.graph.keys())
        classified_nodes = self.proveedores | self.intermedios | self.consumidores
        
        unclassified = all_graph_nodes - classified_nodes
        if unclassified:
            self.violations.append({
                "type": "UNCLASSIFIED_NODES",
                "severity": "HIGH",
                "description": f"Los siguientes nodos no están clasificados: {sorted(unclassified)}",
                "nodes": sorted(unclassified)
            })
        
        # Verificar nodos clasificados que no existen en el grafo
        extra_nodes = classified_nodes - all_graph_nodes
        if extra_nodes:
            self.violations.append({
                "type": "EXTRA_CLASSIFIED_NODES",
                "severity": "MEDIUM",
                "description": f"Los siguientes nodos están clasificados pero no existen en el grafo: {sorted(extra_nodes)}",
                "nodes": sorted(extra_nodes)
            })
    
    def _validate_classification_overlap(self):
        """
        Verifica que un nodo no esté en más de una categoría.
        """
        categories = {
            "proveedores": self.proveedores,
            "intermedios": self.intermedios,
            "consumidores": self.consumidores
        }
        
        # Verificar intersecciones entre pares de categorías
        overlaps = []
        category_names = list(categories.keys())
        
        for i in range(len(category_names)):
            for j in range(i + 1, len(category_names)):
                cat1 = category_names[i]
                cat2 = category_names[j]
                intersection = categories[cat1] & categories[cat2]
                if intersection:
                    overlaps.append({
                        "categories": (cat1, cat2),
                        "nodes": sorted(intersection)
                    })
        
        # Verificar intersección triple
        triple_overlap = self.proveedores & self.intermedios & self.consumidores
        if triple_overlap:
            overlaps.append({
                "categories": ("proveedores", "intermedios", "consumidores"),
                "nodes": sorted(triple_overlap)
            })
        
        if overlaps:
            for overlap in overlaps:
                self.violations.append({
                    "type": "CLASSIFICATION_OVERLAP",
                    "severity": "CRITICAL",
                    "description": f"Superposición en categorías {overlap['categories']}: {overlap['nodes']}",
                    "nodes": overlap["nodes"],
                    "categories": overlap["categories"]
                })
    
    def audit(self):
        """
        Ejecuta la auditoría completa de la cadena de suministro.
        
        Returns:
            dict: Reporte detallado de violaciones encontradas
        """
        self.violations = []
        
        # Primero validar clasificaciones
        self._validate_classification_completeness()
        self._validate_classification_overlap()
        
        # Validar reglas de negocio para cada nodo
        self._validate_business_rules()
        
        # Verificar integridad del grafo
        self._validate_graph_integrity()
        
        # Generar resumen del reporte
        return self._generate_report()
    
    def _validate_business_rules(self):
        """
        Verifica las reglas de negocio:
        - Proveedores no deben tener conexiones de entrada
        - Consumidores no deben tener conexiones de salida
        - Intermedios deben tener al menos una entrada y una salida
        """
        # Verificar proveedores
        for proveedor in self.proveedores:
            if proveedor in self.graph:
                # Verificar conexiones de entrada
                has_input = self._has_incoming_edges(proveedor)
                if has_input:
                    incoming_from = self._get_incoming_nodes(proveedor)
                    self.violations.append({
                        "type": "PROVEEDOR_WITH_INPUT",
                        "severity": "CRITICAL",
                        "node": proveedor,
                        "description": f"El proveedor '{proveedor}' tiene conexiones de entrada desde: {incoming_from}",
                        "incoming_from": incoming_from
                    })
        
        # Verificar consumidores
        for consumidor in self.consumidores:
            if consumidor in self.graph:
                # Verificar conexiones de salida
                if self.graph.get(consumidor, []):
                    outgoing_to = self.graph[consumidor]
                    self.violations.append({
                        "type": "CONSUMIDOR_WITH_OUTPUT",
                        "severity": "CRITICAL",
                        "node": consumidor,
                        "description": f"El consumidor '{consumidor}' tiene conexiones de salida hacia: {outgoing_to}",
                        "outgoing_to": outgoing_to
                    })
        
        # Verificar intermedios
        for intermedio in self.intermedios:
            if intermedio in self.graph:
                has_input = self._has_incoming_edges(intermedio)
                has_output = bool(self.graph.get(intermedio, []))
                
                if not has_input and not has_output:
                    self.violations.append({
                        "type": "INTERMEDIO_ISOLATED",
                        "severity": "HIGH",
                        "node": intermedio,
                        "description": f"El intermedio '{intermedio}' está aislado (sin entrada ni salida)"
                    })
                elif not has_input:
                    self.violations.append({
                        "type": "INTERMEDIO_NO_INPUT",
                        "severity": "HIGH",
                        "node": intermedio,
                        "description": f"El intermedio '{intermedio}' tiene salidas pero no tiene entradas"
                    })
                elif not has_output:
                    self.violations.append({
                        "type": "INTERMEDIO_NO_OUTPUT",
                        "severity": "HIGH",
                        "node": intermedio,
                        "description": f"El intermedio '{intermedio}' tiene entradas pero no tiene salidas"
                    })
    
    def _validate_graph_integrity(self):
        """
        Verifica la integridad estructural del grafo.
        """
        all_nodes = set(self.graph.keys())
        
        # Verificar nodos que aparecen como destino pero no como origen
        all_destinations = set()
        for origin, destinations in self.graph.items():
            all_destinations.update(destinations)
        
        missing_origin_nodes = all_destinations - all_nodes
        if missing_origin_nodes:
            self.violations.append({
                "type": "MISSING_ORIGIN_NODES",
                "severity": "MEDIUM",
                "description": f"Los siguientes nodos aparecen como destino pero no como origen: {sorted(missing_origin_nodes)}",
                "nodes": sorted(missing_origin_nodes)
            })
        
        # Verificar ciclos en el grafo (opcional, puede ser válido en algunas cadenas)
        cycles = self._detect_cycles()
        if cycles:
            self.violations.append({
                "type": "CYCLES_DETECTED",
                "severity": "MEDIUM",
                "description": f"Se detectaron ciclos en la cadena de suministro: {cycles}",
                "cycles": cycles
            })
    
    def _has_incoming_edges(self, node):
        """
        Verifica si un nodo tiene conexiones de entrada.
        """
        for origin, destinations in self.graph.items():
            if node in destinations:
                return True
        return False
    
    def _get_incoming_nodes(self, node):
        """
        Retorna los nodos que tienen conexiones hacia el nodo especificado.
        """
        incoming = []
        for origin, destinations in self.graph.items():
            if node in destinations:
                incoming.append(origin)
        return sorted(incoming)
    
    def _detect_cycles(self):
        """
        Detecta ciclos en el grafo dirigido usando DFS.
        """
        visited = set()
        rec_stack = set()
        cycles = []
        
        def dfs(node, path):
            if node in rec_stack:
                # Encontrar el ciclo en el path
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                cycles.append(cycle)
                return
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.graph.get(node, []):
                dfs(neighbor, path.copy())
            
            rec_stack.remove(node)
            path.pop()
        
        for node in self.graph:
            if node not in visited:
                dfs(node, [])
        
        return cycles
    
    def _generate_report(self):
        """
        Genera un reporte estructurado de la auditoría.
        """
        # Contar violaciones por severidad
        severity_counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }
        
        for violation in self.violations:
            severity = violation.get("severity", "LOW")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Agrupar violaciones por tipo
        violations_by_type = {}
        for violation in self.violations:
            vtype = violation["type"]
            if vtype not in violations_by_type:
                violations_by_type[vtype] = []
            violations_by_type[vtype].append(violation)
        
        # Calcular estadísticas de la red
        total_nodes = len(self.graph)
        total_edges = sum(len(dest) for dest in self.graph.values())
        
        return {
            "status": "FAIL" if self.violations else "PASS",
            "summary": {
                "total_violations": len(self.violations),
                "critical_violations": severity_counts["CRITICAL"],
                "high_violations": severity_counts["HIGH"],
                "medium_violations": severity_counts["MEDIUM"],
                "low_violations": severity_counts["LOW"]
            },
            "network_stats": {
                "total_nodes": total_nodes,
                "total_edges": total_edges,
                "proveedores_count": len(self.proveedores),
                "intermedios_count": len(self.intermedios),
                "consumidores_count": len(self.consumidores)
            },
            "violations_by_type": violations_by_type,
            "all_violations": self.violations
        }


def audit_supply_chain(graph, proveedores, intermedios, consumidores, verbose=True):
    """
    Función independiente para auditar una cadena de suministro.
    
    Args:
        graph: Diccionario con formato {nodo: [lista_de_vecinos]}
        proveedores: Lista de nodos clasificados como proveedores
        intermedios: Lista de nodos clasificados como intermedios
        consumidores: Lista de nodos clasificados como consumidores
        verbose: Si es True, imprime el reporte detallado
    
    Returns:
        dict: Reporte de auditoría
    """
    auditor = SupplyChainAuditor()
    auditor.load_network(graph, proveedores, intermedios, consumidores)
    report = auditor.audit()
    
    if verbose:
        print_audit_report(report)
    
    return report


def print_audit_report(report):
    """
    Imprime el reporte de auditoría de forma legible.
    """
    print("=" * 70)
    print("AUDITORIA DE CADENA DE SUMINISTRO")
    print("=" * 70)
    
    # Estado general
    status = report["status"]
    if status == "PASS":
        print("ESTADO: APROBADA - No se encontraron violaciones")
    else:
        print(f"ESTADO: RECHAZADA - Se encontraron {report['summary']['total_violations']} violaciones")
    
    print("-" * 70)
    
    # Estadísticas de red
    stats = report["network_stats"]
    print("ESTADISTICAS DE RED:")
    print(f"  Total de nodos: {stats['total_nodes']}")
    print(f"  Total de arcos: {stats['total_edges']}")
    print(f"  Proveedores: {stats['proveedores_count']}")
    print(f"  Intermedios: {stats['intermedios_count']}")
    print(f"  Consumidores: {stats['consumidores_count']}")
    
    print("-" * 70)
    
    # Resumen de violaciones por severidad
    summary = report["summary"]
    if summary["total_violations"] > 0:
        print("VIOLACIONES POR SEVERIDAD:")
        print(f"  CRITICAL: {summary['critical_violations']}")
        print(f"  HIGH: {summary['high_violations']}")
        print(f"  MEDIUM: {summary['medium_violations']}")
        print(f"  LOW: {summary['low_violations']}")
        
        print("-" * 70)
        print("DETALLE DE VIOLACIONES:")
        print("-" * 70)
        
        # Mostrar violaciones agrupadas por severidad
        severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        for severity in severity_order:
            severity_violations = [v for v in report["all_violations"] if v.get("severity") == severity]
            if severity_violations:
                print(f"\n{severity} VIOLATIONS ({len(severity_violations)}):")
                for idx, violation in enumerate(severity_violations, 1):
                    print(f"  {idx}. {violation['description']}")
    else:
        print("No se encontraron violaciones en la cadena de suministro.")
    
    print("=" * 70)

# Pruebas:
# Ejemplo 1: Cadena de suministro válida
print("CADENA VALIDA")
print("-" * 50)

valid_graph = {
    "Proveedor1": ["Intermedio1", "Intermedio2"],
    "Proveedor2": ["Intermedio1"],
    "Intermedio1": ["Intermedio3", "Consumidor1"],
    "Intermedio2": ["Intermedio3"],
    "Intermedio3": ["Consumidor2"],
    "Consumidor1": [],
    "Consumidor2": []
}

proveedores = ["Proveedor1", "Proveedor2"]
intermedios = ["Intermedio1", "Intermedio2", "Intermedio3"]
consumidores = ["Consumidor1", "Consumidor2"]

report1 = audit_supply_chain(valid_graph, proveedores, intermedios, consumidores)

# Ejemplo 2: Cadena con violaciones
print("\n\nCADENA CON VIOLACIONES")
print("-" * 50)

invalid_graph = {
    "Proveedor1": ["Intermedio1"],
    "Proveedor2": [],  # Proveedor sin salidas (ok)
    "Intermedio1": ["Proveedor1"],  # Esto crea un ciclo
    "Intermedio2": ["Consumidor1"],  # Intermedio sin entrada
    "Consumidor1": ["Intermedio3"],  # Consumidor con salida (violación)
    "Intermedio3": [],  # Intermedio aislado
    "NodoNoClasificado": ["Intermedio1"]  # Nodo sin clasificación
}

proveedores_invalid = ["Proveedor1", "Proveedor2"]
intermedios_invalid = ["Intermedio1", "Intermedio2", "Intermedio3"]
consumidores_invalid = ["Consumidor1"]

report2 = audit_supply_chain(invalid_graph, proveedores_invalid, intermedios_invalid, consumidores_invalid)

# Ejemplo 3: Acceso programático al reporte
print("\n\nACCESO PROGRAMATICO")
print("-" * 50)

graph_simple = {
    "P1": ["I1"],
    "I1": ["C1"],
    "C1": []
}

result = audit_supply_chain(graph_simple, ["P1"], ["I1"], ["C1"], verbose=False)

print("Estado:", result["status"])
print("Total violaciones:", result["summary"]["total_violations"])
print("Nodos totales:", result["network_stats"]["total_nodes"])
print("Arcos totales:", result["network_stats"]["total_edges"])

if result["violations_by_type"]:
    print("\nViolaciones por tipo:")
    for vtype, violations in result["violations_by_type"].items():
        print(f"  {vtype}: {len(violations)}")

# Ejemplo 4: Usando la clase directamente para auditoría más controlada
print("\n\nUSO DE CLASE DIRECTA")
print("-" * 50)

auditor = SupplyChainAuditor()
auditor.load_network(invalid_graph, proveedores_invalid, intermedios_invalid, consumidores_invalid)
report_direct = auditor.audit()

# Filtrar solo violaciones críticas
critical_violations = [v for v in report_direct["all_violations"] if v["severity"] == "CRITICAL"]
print(f"Violaciones críticas encontradas: {len(critical_violations)}")
for violation in critical_violations:
    print(f"  - {violation['type']}: {violation['description']}")
