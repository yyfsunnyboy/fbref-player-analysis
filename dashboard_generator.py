# -*- coding: utf-8 -*-
"""
eFootball 球員狀態儀表板生成器 v8.4 (戰術分析版 - 最終修正)
功能：
1. 【核心修正】修復了因 xlwings API 語法問題導致的圖表生成錯誤。
2. 將「組織能力」圖表拆分為兩個獨立、清晰的圖表，以提高穩定性與可讀性。
3. 持續優化數據讀取與處理的穩健性。
"""

import pandas as pd
import xlwings as xw

def extract_table_from_sheet(sheet, header_keywords):
    """
    讀取整個工作表，然後根據表頭關鍵字列表，精準地提取出對應的數據表格。
    """
    try:
        full_df = sheet.used_range.options(pd.DataFrame, header=False, index=False).value
        
        header_row_index = -1
        found_keyword = ""
        for i, row in full_df.iterrows():
            if row.astype(str).str.contains('|'.join(header_keywords), na=False).any():
                header_row_index = i
                found_keyword = [k for k in header_keywords if row.astype(str).str.contains(k, na=False).any()][0]
                break
        
        if header_row_index == -1:
            print(f"  > 警告：在工作表 '{sheet.name}' 中找不到包含 {header_keywords} 的表頭。")
            return None

        print(f"  > 在第 {header_row_index + 1} 列找到 '{found_keyword}' 表頭，正在提取表格...")
        
        headers = full_df.iloc[header_row_index]
        data_df = full_df.iloc[header_row_index + 1:].copy()
        data_df.columns = headers
        
        data_df.dropna(how='all', axis=0, inplace=True)
        data_df.dropna(how='all', axis=1, inplace=True)
        data_df.reset_index(drop=True, inplace=True)
        
        return data_df

    except Exception as e:
        print(f"  > 提取表格 '{header_keywords}' 時發生錯誤: {e}")
    return None

def create_player_dashboard(excel_path, players_to_analyze):
    """主函式，用於創建儀表板"""
    
    print("=== 開始創建「戰術分析」儀表板 ===")
    
    app = None
    try:
        app = xw.App(visible=False)
        workbook = app.books.open(excel_path)
        print(f"✅ 成功開啟 Excel 檔案: '{excel_path}'")

        all_sheet_names = [s.name for s in workbook.sheets]
        
        print(f"� 將針對指定的 {len(players_to_analyze)} 位球員進行深度分析...")

        dashboard_data = []
        
        for player_name in players_to_analyze:
            try:
                if player_name not in all_sheet_names:
                    print(f"\n--- 警告：在 Excel 中找不到名為 '{player_name}' 的工作表，已跳過。 ---")
                    continue

                sheet = workbook.sheets[player_name]
                print(f"\n--- 正在分析球員: {player_name} ---")
                
                match_log_df = extract_table_from_sheet(sheet, header_keywords=["Match Report", "Date"])
                
                # --- 分析近期狀態 (最近5場) ---
                last_5_goals, last_5_assists = 0, 0
                last_5_tkl, last_5_int, last_5_blocks = 0, 0, 0
                last_5_cmp, last_5_att, last_5_prgp = 0, 0, 0

                if match_log_df is not None and not match_log_df.empty:
                    passing_cols_mapping = {
                        'Cmp': ['Cmp', 'Cmp.1', 'Cmp.2', 'Cmp.3'],
                        'Att': ['Att', 'Att.1', 'Att.2', 'Att.3'],
                        'PrgP': ['PrgP']
                    }
                    
                    numeric_cols = ['Gls', 'Ast', 'Tkl', 'Int', 'Blocks']
                    for col_list in passing_cols_mapping.values():
                        numeric_cols.extend(col_list)
                    
                    for col in numeric_cols:
                        if col in match_log_df.columns:
                            target_data = match_log_df[col]
                            if isinstance(target_data, pd.DataFrame):
                                match_log_df[col] = target_data.apply(lambda x: pd.to_numeric(x, errors='coerce')).fillna(0)
                            else:
                                match_log_df[col] = pd.to_numeric(target_data, errors='coerce').fillna(0)
                    
                    if 'Min' in match_log_df.columns:
                        match_log_df['Min'] = pd.to_numeric(match_log_df['Min'], errors='coerce').fillna(0)
                        played_games = match_log_df[match_log_df['Min'] > 0].copy()
                    else:
                        played_games = match_log_df.copy()
                    
                    if not played_games.empty:
                        last_5_games = played_games.tail(5)
                        last_5_goals = last_5_games['Gls'].sum() if 'Gls' in last_5_games.columns else 0
                        last_5_assists = last_5_games['Ast'].sum() if 'Ast' in last_5_games.columns else 0
                        last_5_tkl = last_5_games['Tkl'].sum() if 'Tkl' in last_5_games.columns else 0
                        last_5_int = last_5_games['Int'].sum() if 'Int' in last_5_games.columns else 0
                        last_5_blocks = last_5_games['Blocks'].sum() if 'Blocks' in last_5_games.columns else 0
                        
                        actual_cmp_cols = [c for c in passing_cols_mapping['Cmp'] if c in last_5_games.columns]
                        actual_att_cols = [c for c in passing_cols_mapping['Att'] if c in last_5_games.columns]
                        actual_prgp_cols = [c for c in passing_cols_mapping['PrgP'] if c in last_5_games.columns]
                        
                        last_5_cmp = last_5_games[actual_cmp_cols].sum().sum() if actual_cmp_cols else 0
                        last_5_att = last_5_games[actual_att_cols].sum().sum() if actual_att_cols else 0
                        last_5_prgp = last_5_games[actual_prgp_cols].sum().sum() if actual_prgp_cols else 0
                
                pass_completion_rate = (last_5_cmp / last_5_att * 100) if last_5_att > 0 else 0

                player_stats = {
                    "球員": player_name,
                    "近期進攻參與 (G+A)": int(last_5_goals + last_5_assists),
                    "防守綜合貢獻 (Tkl+Int+Blocks)": int(last_5_tkl + last_5_int + last_5_blocks),
                    "近5場傳球成功率 (%)": round(pass_completion_rate, 1),
                    "近5場漸進式傳球 (PrgP)": int(last_5_prgp),
                }
                dashboard_data.append(player_stats)
                print(f"  > 已整合近期狀態分析: {player_name}")

            except Exception as e:
                print(f"⚠️ 分析球員 {player_name} 時發生嚴重錯誤: {e}，已跳過。")

        if not dashboard_data:
            print("❌ 未能成功分析任何球員數據，無法生成儀表板。")
            return

        dashboard_sheet_name = "球員儀表板 (Dashboard)"
        if dashboard_sheet_name in [s.name for s in workbook.sheets]:
            dashboard_sheet = workbook.sheets[dashboard_sheet_name]
            dashboard_sheet.clear()
        else:
            dashboard_sheet = workbook.sheets.add(dashboard_sheet_name, after=workbook.sheets[0])
        
        dashboard_sheet.activate()
        print("\n📊 正在生成「戰術分析」儀表板...")
        
        dashboard_df = pd.DataFrame(dashboard_data)
        
        dashboard_sheet.range('B2').value = "球員戰術儀表板 (近期狀態分析)"
        dashboard_sheet.range('B2').font.bold = True
        dashboard_sheet.range('B2').font.size = 24
        
        table_range_start = dashboard_sheet.range('B4')
        table_range_start.options(pd.DataFrame, index=False, header=True).value = dashboard_df
        
        table_range = table_range_start.expand('table')
        table = dashboard_sheet.tables.add(source=table_range, name="PlayerDashboard")
        table.table_style_name = 'TableStyleMedium4'
        
        for col_name in ["近期進攻參與 (G+A)", "防守綜合貢獻 (Tkl+Int+Blocks)", "近5場漸進式傳球 (PrgP)"]:
            if col_name in dashboard_df.columns:
                col_index = dashboard_df.columns.get_loc(col_name) + table_range.column
                column_range = dashboard_sheet.range((table_range.row + 1, col_index), (table_range.last_cell.row, col_index))
                column_range.api.FormatConditions.AddColorScale(3)
        
        chart_top = table_range.top + table_range.height + 20
        chart_width = 700
        chart_height = 400
        
        # 【核心修正】圖表1: 攻守綜合貢獻 (堆疊圖)
        chart1 = dashboard_sheet.charts.add(left=table_range.left, top=chart_top, width=chart_width, height=chart_height)
        player_col_idx = dashboard_df.columns.get_loc("球員") + table_range.column
        ga_col_idx = dashboard_df.columns.get_loc("近期進攻參與 (G+A)") + table_range.column
        def_col_idx = dashboard_df.columns.get_loc("防守綜合貢獻 (Tkl+Int+Blocks)") + table_range.column
        
        player_range_address = dashboard_sheet.range((table_range.row, player_col_idx), (table_range.last_cell.row, player_col_idx)).address
        # 選擇攻守兩個數據欄位
        contribution_data_range_address = dashboard_sheet.range((table_range.row, ga_col_idx), (table_range.last_cell.row, def_col_idx)).address
        chart1_source_address = f'({player_range_address},{contribution_data_range_address})'
        
        chart1.set_source_data(dashboard_sheet.range(chart1_source_address))
        chart1.chart_type = 'column_stacked' # 使用堆疊圖來呈現總貢獻
        chart1.name = "近期攻守綜合貢獻 (近5場)"
        
        # 【核心修正】圖表2: 組織能力 (漸進式傳球) - 單獨顯示
        chart2 = dashboard_sheet.charts.add(left=chart1.left + chart1.width + 20, top=chart_top, width=chart_width, height=chart_height)
        prgp_data_col_idx = dashboard_df.columns.get_loc("近5場漸進式傳球 (PrgP)") + table_range.column
        
        prgp_data_range_address = dashboard_sheet.range((table_range.row, prgp_data_col_idx), (table_range.last_cell.row, prgp_data_col_idx)).address
        chart2_source_address = f'({player_range_address},{prgp_data_range_address})'
        
        chart2.set_source_data(dashboard_sheet.range(chart2_source_address))
        chart2.chart_type = 'bar_clustered'
        chart2.name = "近期組織能力 (漸進式傳球次數)"

        dashboard_sheet.autofit()
        
        workbook.save()
        print("✅ 儀表板已成功創建並儲存！")

    except Exception as e:
        print(f"❌ 發生嚴重錯誤: {e}")
    finally:
        if app:
            app.quit()
            
if __name__ == "__main__":
    player_list = [
        "Ruben Dias", "Josko Gvardiol", "Kevin De Bruyne", "Mateo Kovacic",
        "Bernardo Silva", "Erling Haaland", "Jamal Musiala", 
        "Robert Lewandowski", "Lamine Yamal"
    ]
    
    create_player_dashboard(
        excel_path='man city player.xlsx',
        players_to_analyze=player_list
    )