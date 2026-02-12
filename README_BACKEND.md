# 📊 Trading Analytics Platform – Backend Documentation
**Versión:** v1 (MVP técnico)
**Stack:** Django + Django Rest Framework + PostgreSQL  
**Arquitectura:** Service-Oriented + REST API  
**Estado:** Estable / Base para crecimiento

---

## 🎯 Objetivo del Proyecto

Este proyecto es una plataforma backend diseñada para:

- Registrar señales de trading (copy trading)
- Registrar operaciones reales (trades)
- Analizar resultados reales y teóricos
- Simular escenarios futuros (proyecciones)
- Ayudar al usuario a tomar mejores decisiones
- Mantener separación clara entre datos, lógica y presentación

El sistema está pensado para:
- Uso personal
- Uso por pocos usuarios
- Escalar en el futuro a un producto comercial (SaaS)

⚠️ **Importante:**  
La plataforma **NO ejecuta trades automáticamente**, solo **analiza y sugiere**.

---

## 🧱 Arquitectura General

El backend sigue una arquitectura por capas:

```
ViewSets (API / Orquestación)
             ↓
Services (Lógica de negocio y cálculos)
             ↓
Models (Persistencia)
```

Principios clave:
- ❌ Nada de lógica compleja en modelos
- ❌ Nada de cálculos en serializers
- ✅ Servicios reutilizables y testeables
- ✅ API clara y consistente

---

## 📦 Apps del Proyecto

El proyecto está dividido en las siguientes apps:

- accounts/
- signals/
- assets/
- trades/
- analytics/
- core/


Cada app tiene una responsabilidad clara.

---

# 👤 accounts – Usuarios y Configuración

Gestiona usuarios, perfiles y preferencias.

### Modelos
- `User`  
  Usuario principal del sistema (email como login).

- `UserProfile`  
  Información personal y contextual del usuario.

- `UserTradingPreference`  
  Preferencias de trading (estilo, sesiones, automatismos).

- `UserRiskProfile`  
  Perfil de riesgo del usuario.

- `UserNotificationSetting`  
  Configuración de notificaciones.

### Rol de la app
- Autenticación
- Personalización del sistema
- Base para multiusuario / SaaS

---

# 📡 signals – Señales de Trading

Gestiona señales de trading externas (copy trading).

### Modelos
- `SignalSource`  
  Grupo, canal o comunidad que envía señales.

- `SignalProvider`  
  Instructor o proveedor dentro de un grupo.

- `TradingSignal`  
  Señal individual (BUY / SELL, SL, TP, etc.).

- `SignalTakeProfit`  
  Múltiples niveles de take profit por señal.

- `SignalContext`  
  Contexto de mercado (volatilidad, sesión, etc.).

### Conceptos clave
- Las señales son **neutrales**
- No pertenecen al usuario
- El usuario decide si las sigue o ignora

---

# $ assets – Activos Operables

Define qué instrumentos se pueden operar.

### Modelos
- `AssetType`  
  Tipo de activo (Forex, Crypto, Commodities).

- `Asset`  
  Activo específico (XAUUSD, BTCUSDT).

- `AssetTradingSchedule`  
  Horarios de trading por activo.

- `AssetSwap`  
  Configuración de swaps y costos overnight.

### Rol
- Normalizar reglas de mercado
- Evitar lógica hardcodeada por activo

---

# 📈 trades – Operaciones Reales

Gestiona la ejecución real del usuario.

### Modelos
- `TradeAccount`  
  Cuenta de trading del usuario.

- `Trade`  
  Contenedor lógico de una operación.

- `TradeEntry`  
  Entradas (scaling in).

- `TradeClose`  
  Cierres parciales o totales.

- `TradeCloseResult`  
  Resultado financiero de cada cierre.

- `TradeCost`  
  Costos asociados (swap, comisión, fee).

### Conceptos clave
- Un trade puede tener:
  - múltiples entradas
  - múltiples cierres
- Soporta:
  - cierres manuales (UI)
  - cierres automáticos (sistema)
- Todo es auditable

---

# 📊 analytics – Análisis y Simulación

Motor de inteligencia del sistema.

### Modelos
- `AnalyticsSnapshot`  
  Foto histórica de rendimiento (semanal/mensual).

- `SignalPerformance`  
  Resultado teórico de una señal.

- `UserSignalStats`  
  Estadísticas por usuario, grupo o proveedor.

- `ProjectionScenario`  
  Escenarios de simulación futura.

- `AnalyticsRun`  
  Registro de ejecuciones analíticas.

---

## 🧠 Services (Capa de Inteligencia)

La lógica vive aquí, no en los modelos.

### Servicios principales
- `TradeMetricsService`
  - PnL real
  - Duración de trades

- `EquityCurveService`
  - Curva de equity trade por trade

- `DrawdownService`
  - Drawdown máximo real

- `SnapshotService`
  - Generación de snapshots

- `ProjectionSimulationService`
  - Simulación realista trade por trade
  - Ajuste de riesgo / balance

- `SignalAccuracyService`
  - Precisión histórica de señales

- `SignalSuggestionService`
  - Sugerencias inteligentes (seguir / ignorar)

---

## 🔁 Custom Actions (API Avanzada)

El sistema expone acciones avanzadas sin romper REST.

### Analytics
- `run_simulation`
- `compare_scenarios`
- `generate_snapshot`
- `equity_curve`

### Trades
- `close_trade`
- `partial_close`
- `summary`
- `recalculate`

### Signals
- `follow`
- `ignore`
- `evaluate`
- `accuracy_by_source`
- `accuracy_by_provider`
- `suggestion`

---

## 🤖 Decisiones del Usuario (Conceptual)

El sistema permite:
- Seguir una señal
- Ignorar una señal
- Configurar reglas futuras

Las decisiones:
- No modifican la señal
- Se usan para analytics
- Permiten aprendizaje real

---

## 🔐 Seguridad y Alcance

- Multiusuario
- Auditable
- Sin ejecución automática
- Enfocado en análisis y decisión

---

## 🚀 Estado del Proyecto (v1)

### Incluye
- Backend completo
- API funcional
- Simulación realista
- Base sólida para frontend

### No incluye (aún)
- Frontend (Angular)
- Permisos avanzados
- Tests automatizados
- Integraciones externas

---

## 📌 Conclusión

Este backend:
- Es estable
- Es extensible
- Es honesto con el usuario
- Está listo para crecer

Primero como herramienta personal, luego como producto.

---

**Autor:** Nicolas Fernandez
**Estado:** MVP Técnico Cerrado
**Siguiente etapa:** Frontend / Uso real / Feedback

