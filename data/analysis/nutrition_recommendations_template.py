#!/usr/bin/env python3
"""
Шаблон для генерации рекомендаций по питанию на основе анализов
Использует данные из knowledge_base.json
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


def load_knowledge_base() -> Dict:
    """Загружает базу знаний"""
    kb_path = Path(__file__).parent.parent.parent / "knowledge_base.json"
    with open(kb_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_latest_blood_test() -> Optional[Dict]:
    """Получает последний свежий анализ крови"""
    kb = load_knowledge_base()
    
    # Фильтруем свежие анализы
    fresh_tests = [
        t for t in kb.get('blood_tests', [])
        if t.get('status') != 'historical'
    ]
    
    if not fresh_tests:
        return None
    
    # Сортируем по дате, берем последний
    latest = max(fresh_tests, key=lambda x: x.get('date', ''))
    return latest


def get_latest_vitamin_test() -> Optional[Dict]:
    """Получает последний анализ витаминов"""
    kb = load_knowledge_base()
    
    vitamins = kb.get('vitamins', [])
    if not vitamins:
        return None
    
    latest = max(vitamins, key=lambda x: x.get('date', ''))
    return latest


def analyze_cholesterol(test: Dict) -> List[Dict]:
    """Анализирует показатели холестерина"""
    recommendations = []
    values = test.get('values', {})
    
    # Общий холестерин
    total_chol = values.get('cholesterol') or values.get('total_cholesterol')
    if total_chol:
        if total_chol > 5.2:
            recommendations.append({
                "indicator": "Общий холестерин",
                "value": total_chol,
                "status": "выше нормы",
                "recommendations": [
                    "Уменьшить насыщенные жиры (красное мясо, сливочное масло)",
                    "Увеличить клетчатку (овощи, фрукты, цельнозерновые)",
                    "Добавить омега-3 (жирная рыба 2-3 раза/неделю, льняное масло)",
                    "Ограничить трансжиры (фастфуд, выпечка)",
                    "Увеличить физическую активность"
                ]
            })
    
    # LDL (плохой холестерин)
    ldl = values.get('LDL') or values.get('ldl')
    if ldl:
        if ldl > 3.0:
            recommendations.append({
                "indicator": "LDL (плохой холестерин)",
                "value": ldl,
                "status": "выше нормы",
                "recommendations": [
                    "Уменьшить красное мясо до 1-2 раз/неделю",
                    "Увеличить рыбу (лосось, скумбрия, сардины)",
                    "Добавить орехи (миндаль, грецкие) - 30г/день",
                    "Овсянка на завтрак (бета-глюканы снижают LDL)",
                    "Авокадо - источник мононенасыщенных жиров"
                ]
            })
    
    # HDL (хороший холестерин)
    hdl = values.get('HDL') or values.get('hdl')
    if hdl:
        if hdl < 1.0:
            recommendations.append({
                "indicator": "HDL (хороший холестерин)",
                "value": hdl,
                "status": "ниже нормы",
                "recommendations": [
                    "Регулярные кардио тренировки (бег, велосипед)",
                    "Умеренное потребление красного вина (если нет противопоказаний)",
                    "Омега-3 добавки",
                    "Оливковое масло вместо других жиров"
                ]
            })
    
    return recommendations


def analyze_vitamins(vitamin_test: Dict) -> List[Dict]:
    """Анализирует показатели витаминов"""
    recommendations = []
    values = vitamin_test.get('values', {})
    
    # Витамин D
    vit_d = values.get('vitamin_d') or values.get('vitamin_D')
    if vit_d:
        if vit_d < 30:
            recommendations.append({
                "indicator": "Витамин D",
                "value": vit_d,
                "status": "ниже нормы",
                "recommendations": [
                    "Добавка витамина D: 2000-4000 МЕ/день",
                    "Жирная рыба (лосось, скумбрия) 2-3 раза/неделю",
                    "Яичные желтки",
                    "Больше времени на солнце (15-20 мин/день)",
                    "Проверить через 3 месяца"
                ]
            })
        elif vit_d < 50:
            recommendations.append({
                "indicator": "Витамин D",
                "value": vit_d,
                "status": "ниже оптимального",
                "recommendations": [
                    "Поддерживающая доза: 1000-2000 МЕ/день",
                    "Регулярное потребление рыбы",
                    "Контроль через 6 месяцев"
                ]
            })
    
    # Витамин B12
    vit_b12 = values.get('vitamin_b12') or values.get('B12')
    if vit_b12:
        if vit_b12 < 200:
            recommendations.append({
                "indicator": "Витамин B12",
                "value": vit_b12,
                "status": "ниже нормы",
                "recommendations": [
                    "Добавка B12 (метилкобаламин) - 1000 мкг/день",
                    "Мясо, рыба, яйца, молочные продукты",
                    "Контроль через 3 месяца"
                ]
            })
    
    return recommendations


def generate_nutrition_plan(recommendations: List[Dict]) -> Dict:
    """Генерирует план питания на основе рекомендаций"""
    plan = {
        "date_created": datetime.now().strftime("%Y-%m-%d"),
        "daily_goals": {},
        "foods_to_increase": [],
        "foods_to_reduce": [],
        "supplements": []
    }
    
    for rec in recommendations:
        for action in rec.get('recommendations', []):
            action_lower = action.lower()
            
            # Определяем категории
            if 'увеличить' in action_lower or 'добавить' in action_lower:
                if 'рыба' in action_lower:
                    plan['foods_to_increase'].append("Жирная рыба (лосось, скумбрия)")
                elif 'овощи' in action_lower or 'клетчатка' in action_lower:
                    plan['foods_to_increase'].append("Овощи и фрукты (минимум 5 порций/день)")
                elif 'орехи' in action_lower:
                    plan['foods_to_increase'].append("Орехи (30г/день)")
                elif 'овсянка' in action_lower:
                    plan['foods_to_increase'].append("Овсянка на завтрак")
            
            if 'уменьшить' in action_lower or 'ограничить' in action_lower:
                if 'мясо' in action_lower:
                    plan['foods_to_reduce'].append("Красное мясо (до 1-2 раз/неделю)")
                elif 'жиры' in action_lower or 'масло' in action_lower:
                    plan['foods_to_reduce'].append("Насыщенные жиры")
            
            if 'добавка' in action_lower or 'витамин' in action_lower:
                if 'd' in action_lower or 'д' in action_lower:
                    plan['supplements'].append("Витамин D: 2000-4000 МЕ/день")
                elif 'b12' in action_lower or 'в12' in action_lower:
                    plan['supplements'].append("Витамин B12: 1000 мкг/день")
                elif 'омега' in action_lower:
                    plan['supplements'].append("Омега-3: 1000-2000 мг/день")
    
    # Убираем дубликаты
    plan['foods_to_increase'] = list(set(plan['foods_to_increase']))
    plan['foods_to_reduce'] = list(set(plan['foods_to_reduce']))
    plan['supplements'] = list(set(plan['supplements']))
    
    return plan


def main():
    """Основная функция"""
    print("🔍 Анализ анализов и генерация рекомендаций по питанию...\n")
    
    # Получаем последние анализы
    blood_test = get_latest_blood_test()
    vitamin_test = get_latest_vitamin_test()
    
    all_recommendations = []
    
    if blood_test:
        print(f"📊 Найден анализ крови от {blood_test.get('date')}")
        chol_recs = analyze_cholesterol(blood_test)
        all_recommendations.extend(chol_recs)
    
    if vitamin_test:
        print(f"💊 Найден анализ витаминов от {vitamin_test.get('date')}")
        vit_recs = analyze_vitamins(vitamin_test)
        all_recommendations.extend(vit_recs)
    
    if not all_recommendations:
        print("⚠️  Не найдено показателей для анализа")
        return
    
    # Генерируем план питания
    nutrition_plan = generate_nutrition_plan(all_recommendations)
    
    # Сохраняем результаты
    output = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "based_on_tests": {
            "blood_test": blood_test.get('date') if blood_test else None,
            "vitamin_test": vitamin_test.get('date') if vitamin_test else None
        },
        "recommendations": all_recommendations,
        "nutrition_plan": nutrition_plan
    }
    
    output_path = Path(__file__).parent / "nutrition_recommendations.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Рекомендации сохранены в {output_path}")
    print(f"\n📋 Резюме:")
    print(f"   - Показателей проанализировано: {len(all_recommendations)}")
    print(f"   - Продуктов для увеличения: {len(nutrition_plan['foods_to_increase'])}")
    print(f"   - Продуктов для уменьшения: {len(nutrition_plan['foods_to_reduce'])}")
    print(f"   - Добавок рекомендовано: {len(nutrition_plan['supplements'])}")


if __name__ == "__main__":
    main()


