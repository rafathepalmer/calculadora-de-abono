import streamlit as st
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import base64
from datetime import datetime

def generate_pdf_report(data):
    """Generate PDF report with calculation results"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1*inch)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Calculadora de Abono para Invernaderos", title_style))
    story.append(Spacer(1, 20))
    
    # Date
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph(f"<b>Fecha del cálculo:</b> {fecha}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Input data table
    input_data = [
        ['Parámetro', 'Valor'],
        ['Número de invernadero', data.get('numero_invernadero', 'No especificado')],
        ['Superficie del invernadero', f"{data['superficie']:.2f} m²"],
        ['Goteros totales', str(data['goteros_totales'])],
        ['Caudal de cada gotero', f"{data['caudal_gotero']:.2f} L×H⁻¹"],
        ['CE del abono', str(data['ce_abono'])],
        ['Tiempo de riego', f"{data['tiempo_riego']:.1f} minutos"]
    ]
    
    input_table = Table(input_data, colWidths=[3*inch, 2*inch])
    input_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(Paragraph("<b>Datos de Entrada:</b>", styles['Heading2']))
    story.append(input_table)
    story.append(Spacer(1, 20))
    
    # Results table
    results_data = [
        ['Resultado', 'Valor'],
        ['Goteros por metro cuadrado', f"{data['goteros_por_metro']:.4f}"],
        ['Litros de agua por hora', f"{data['litros_agua_hora']:.2f} L"],
        ['Caudal cada 1000 m² por hora', f"{data['caudal_1000m2_hora']:.2f} L"],
        ['Cantidad de agua gastada en este riego', f"{data.get('agua_gastada_riego', 0):.2f} L"],
        ['Abono gastado en el riego', f"{data['abono_gastado']:.2f} Kg"]
    ]
    
    results_table = Table(results_data, colWidths=[3*inch, 2*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Bold last row
        ('FONTSIZE', (0, -1), (-1, -1), 11)
    ]))
    
    story.append(Paragraph("<b>Resultados:</b>", styles['Heading2']))
    story.append(results_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def generate_share_text(data):
    """Generate comprehensive text with all data and results for sharing"""
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    share_text = f"""🌱 CALCULADORA DE ABONO PARA INVERNADEROS
Fecha del cálculo: {fecha}

📊 DATOS DE ENTRADA:
• Número de invernadero: {data.get('numero_invernadero', 'No especificado')}
• Superficie del invernadero: {data['superficie']:.2f} m²
• Goteros totales: {data['goteros_totales']}
• Caudal de cada gotero: {data['caudal_gotero']:.2f} L×H⁻¹
• CE del abono: {data['ce_abono']}
• Tiempo de riego: {data['tiempo_riego']:.1f} minutos

📈 RESULTADOS CALCULADOS:
• Goteros por metro cuadrado: {data['goteros_por_metro']:.4f}
• Litros de agua por hora: {data['litros_agua_hora']:.2f} L
• Caudal cada 1000 m² por hora: {data['caudal_1000m2_hora']:.2f} L
• Cantidad de agua gastada en este riego: {data.get('agua_gastada_riego', 0):.2f} L

🎯 RESULTADO FINAL:
• Abono gastado en el riego: {data['abono_gastado']:.2f} Kg

Calculado con: https://calculadora-abono-invernaderos.replit.app"""
    
    return share_text

def main():
    # Modern CSS styling with contemporary design
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #4ade80 0%, #22c55e 50%, #16a34a 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .main-header {
        background: linear-gradient(135deg, #16a34a, #15803d);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1), transparent);
        pointer-events: none;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 600;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        margin: 1rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .section-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1a202c;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
        border: 1px solid rgba(34, 197, 94, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(135deg, #22c55e, #16a34a);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .final-result {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 600;
        box-shadow: 0 10px 30px rgba(34, 197, 94, 0.4);
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .final-result::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #22c55e, #16a34a) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4) !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #64748b, #475569) !important;
        box-shadow: 0 4px 15px rgba(100, 116, 139, 0.3) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        box-shadow: 0 8px 25px rgba(100, 116, 139, 0.4) !important;
    }
    
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 2px solid #e2e8f0 !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1) !important;
    }
    
    .info-section {
        background: linear-gradient(135deg, #eff6ff, #e0f2fe);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        margin-top: 2rem;
    }
    
    .status-message {
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        border: 1px solid #f59e0b;
        color: #92400e;
    }
    
    .status-info {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
        border: 1px solid #3b82f6;
        color: #1e40af;
    }
    
    .status-error {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        border: 1px solid #ef4444;
        color: #dc2626;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """, unsafe_allow_html=True)
    
    # Modern header with glassmorphism effect
    st.markdown("""
    <div class="main-header">
        <h1>🌱 Calculadora de Abono</h1>
        <p>Calcula el gasto de abono en riegos de invernaderos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Datos de Entrada</div>', unsafe_allow_html=True)
        
        # Input fields with session state keys for proper reset functionality
        numero_invernadero = st.text_input(
            "Número de invernadero:",
            value="",
            help="Identificador del invernadero",
            key="numero_invernadero"
        )
        
        superficie = st.number_input(
            "Superficie del invernadero (m²):",
            min_value=0.0,
            value=0.0,
            step=1.0,
            format="%.2f",
            help="Superficie total del invernadero en metros cuadrados",
            key="superficie"
        )
        
        goteros_totales = st.number_input(
            "Goteros totales:",
            min_value=0,
            value=0,
            step=1,
            help="Número total de goteros en el invernadero",
            key="goteros_totales"
        )
        
        caudal_gotero = st.number_input(
            "Caudal de cada gotero (L×H⁻¹):",
            min_value=0.0,
            value=0.0,
            step=0.1,
            format="%.2f",
            help="Caudal de cada gotero en litros por hora",
            key="caudal_gotero"
        )
        
        ce_abono = st.number_input(
            "CE del abono:",
            min_value=0.0,
            value=0.0,
            step=0.1,
            format="%.2f",
            help="Conductividad eléctrica del abono",
            key="ce_abono"
        )
        
        tiempo_riego = st.number_input(
            "Tiempo de riego (minutos):",
            min_value=0.0,
            value=0.0,
            step=1.0,
            format="%.1f",
            help="Duración del riego en minutos",
            key="tiempo_riego"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📈 Resultados Calculados</div>', unsafe_allow_html=True)
        
        # Initialize variables
        goteros_por_metro = 0
        litros_agua_hora = 0
        caudal_1000m2_hora = 0
        abono_gastado = 0
        
        # Validation and calculations
        if superficie > 0 and goteros_totales > 0 and caudal_gotero > 0:
            try:
                # Calculate derived values
                goteros_por_metro = goteros_totales / superficie
                litros_agua_hora = superficie * goteros_por_metro * caudal_gotero
                caudal_1000m2_hora = litros_agua_hora / (superficie / 1000)
                
                # Display derived calculations with modern styling
                st.markdown(f'''
                <div class="metric-card">
                    <h4 style="color: #1a202c; margin: 0; font-weight: 600;">💧 Goteros por metro cuadrado</h4>
                    <p style="font-size: 1.4rem; font-weight: 700; margin: 0.75rem 0; color: #16a34a;">{goteros_por_metro:.4f}</p>
                    <small style="color: #64748b; font-weight: 500;">Goteros totales / Superficie del invernadero</small>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown(f'''
                <div class="metric-card">
                    <h4 style="color: #1a202c; margin: 0; font-weight: 600;">🚰 Litros de agua por hora</h4>
                    <p style="font-size: 1.4rem; font-weight: 700; margin: 0.75rem 0; color: #16a34a;">{litros_agua_hora:.2f} L</p>
                    <small style="color: #64748b; font-weight: 500;">Superficie × Goteros por m² × Caudal de cada gotero</small>
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown(f'''
                <div class="metric-card">
                    <h4 style="color: #1a202c; margin: 0; font-weight: 600;">⚡ Caudal cada 1000 m² por hora</h4>
                    <p style="font-size: 1.4rem; font-weight: 700; margin: 0.75rem 0; color: #16a34a;">{caudal_1000m2_hora:.2f} L</p>
                    <small style="color: #64748b; font-weight: 500;">Litros de agua por hora / (Superficie / 1000)</small>
                </div>
                ''', unsafe_allow_html=True)
                
                # Calculate water consumed for this irrigation
                if tiempo_riego > 0:
                    agua_gastada_riego = ((superficie * goteros_por_metro * caudal_gotero) / 60) * tiempo_riego
                    
                    st.markdown(f'''
                    <div class="metric-card">
                        <h4 style="color: #1a202c; margin: 0; font-weight: 600;">🌊 Cantidad de Agua gastada en este riego</h4>
                        <p style="font-size: 1.4rem; font-weight: 700; margin: 0.75rem 0; color: #16a34a;">{agua_gastada_riego:.2f} L</p>
                        <small style="color: #64748b; font-weight: 500;">((Superficie × Goteros por m² × Caudal) / 60) × Tiempo de riego</small>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Calculate final fertilizer consumption if all parameters are available
                if ce_abono > 0 and tiempo_riego > 0:
                    # Formula: (Caudal cada1000m2 a la hora / 100000) * CE del abono * Tiempo de riego * (Superficie/1000)
                    abono_gastado = (caudal_1000m2_hora / 100000) * ce_abono * tiempo_riego * (superficie / 1000)
                    
                    # Display the final result prominently with custom styling
                    st.markdown(f'''
                    <div class="final-result">
                        <h3 style="margin: 0; color: white;">🎯 Resultado Final</h3>
                        <div style="font-size: 1.5rem; margin-top: 0.5rem;">
                            Abono gastado: <strong>{abono_gastado:.2f} Kg</strong>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    # Action buttons
                    st.markdown("---")
                    col_btn1, col_btn2, col_btn3 = st.columns(3)
                    
                    with col_btn1:
                        # PDF Download button
                        if st.button("📄 Guardar PDF", type="primary"):
                            # Calculate water consumed for PDF
                            agua_gastada_riego = ((superficie * goteros_por_metro * caudal_gotero) / 60) * tiempo_riego if tiempo_riego > 0 else 0
                            
                            pdf_data = {
                                'numero_invernadero': numero_invernadero,
                                'superficie': superficie,
                                'goteros_totales': goteros_totales,
                                'caudal_gotero': caudal_gotero,
                                'ce_abono': ce_abono,
                                'tiempo_riego': tiempo_riego,
                                'goteros_por_metro': goteros_por_metro,
                                'litros_agua_hora': litros_agua_hora,
                                'caudal_1000m2_hora': caudal_1000m2_hora,
                                'agua_gastada_riego': agua_gastada_riego,
                                'abono_gastado': abono_gastado
                            }
                            
                            try:
                                pdf_bytes = generate_pdf_report(pdf_data)
                                fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M")
                                nombre_archivo = f"calculo_abono_{numero_invernadero}_{fecha_archivo}.pdf" if numero_invernadero else f"calculo_abono_{fecha_archivo}.pdf"
                                
                                st.download_button(
                                    label="⬇️ Descargar PDF",
                                    data=pdf_bytes,
                                    file_name=nombre_archivo,
                                    mime="application/pdf"
                                )
                            except Exception as e:
                                st.error(f"Error generando PDF: {str(e)}")
                    
                    with col_btn2:
                        # Share button
                        if st.button("🔗 Compartir"):
                            # Calculate water consumed for sharing
                            agua_gastada_riego = ((superficie * goteros_por_metro * caudal_gotero) / 60) * tiempo_riego if tiempo_riego > 0 else 0
                            
                            share_data = {
                                'numero_invernadero': numero_invernadero,
                                'superficie': superficie,
                                'goteros_totales': goteros_totales,
                                'caudal_gotero': caudal_gotero,
                                'ce_abono': ce_abono,
                                'tiempo_riego': tiempo_riego,
                                'goteros_por_metro': goteros_por_metro,
                                'litros_agua_hora': litros_agua_hora,
                                'caudal_1000m2_hora': caudal_1000m2_hora,
                                'agua_gastada_riego': agua_gastada_riego,
                                'abono_gastado': abono_gastado
                            }
                            
                            try:
                                # Generate PDF
                                pdf_bytes = generate_pdf_report(share_data)
                                fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M")
                                nombre_archivo = f"calculo_abono_{numero_invernadero}_{fecha_archivo}.pdf" if numero_invernadero else f"calculo_abono_{fecha_archivo}.pdf"
                                
                                # Create sharing options
                                st.markdown("### 📤 Compartir Resultados")
                                
                                # Download PDF first
                                st.download_button(
                                    label="📄 Descargar PDF para compartir",
                                    data=pdf_bytes,
                                    file_name=nombre_archivo,
                                    mime="application/pdf",
                                    key="share_download"
                                )
                                
                                # Base64 encode PDF for sharing links
                                pdf_b64 = base64.b64encode(pdf_bytes).decode()
                                
                                # Sharing text for social media
                                share_text = f"🌱 Resultados de mi cálculo de abono para invernaderos:\n\n"
                                share_text += f"📊 Invernadero: {numero_invernadero if numero_invernadero else 'No especificado'}\n"
                                share_text += f"🎯 Abono gastado: {abono_gastado:.2f} Kg\n"
                                share_text += f"💧 Agua gastada: {agua_gastada_riego:.2f} L\n\n"
                                share_text += "Calculado con: https://calculadora-abono-invernaderos.replit.app"
                                
                                # Create sharing buttons
                                col_email, col_whatsapp, col_telegram = st.columns(3)
                                
                                with col_email:
                                    email_subject = "Resultados Calculadora de Abono"
                                    email_body = share_text.replace('\n', '%0D%0A')
                                    email_link = f"mailto:?subject={email_subject}&body={email_body}"
                                    st.markdown(f'<a href="{email_link}" target="_blank"><button style="background: #4CAF50; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; width: 100%;">📧 Email</button></a>', unsafe_allow_html=True)
                                
                                with col_whatsapp:
                                    whatsapp_text = share_text.replace('\n', '%0A')
                                    whatsapp_link = f"https://wa.me/?text={whatsapp_text}"
                                    st.markdown(f'<a href="{whatsapp_link}" target="_blank"><button style="background: #25D366; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; width: 100%;">📱 WhatsApp</button></a>', unsafe_allow_html=True)
                                
                                with col_telegram:
                                    telegram_text = share_text.replace('\n', '%0A')
                                    telegram_link = f"https://t.me/share/url?text={telegram_text}"
                                    st.markdown(f'<a href="{telegram_link}" target="_blank"><button style="background: #0088cc; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; width: 100%;">✈️ Telegram</button></a>', unsafe_allow_html=True)
                                
                                st.info("💡 Primero descarga el PDF, luego usa los botones para compartir el resumen por redes sociales")
                                
                            except Exception as e:
                                st.error(f"Error generando PDF para compartir: {str(e)}")
                    
                    with col_btn3:
                        # Reset button
                        if st.button("🔄 Reiniciar", type="secondary"):
                            # Clear all session state values
                            for key in st.session_state.keys():
                                del st.session_state[key]
                            st.rerun()
                else:
                    st.markdown('''
                    <div style="background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 1rem; border-radius: 8px; text-align: center;">
                        ⚠️ Introduce la CE del abono y el tiempo de riego para calcular el abono gastado
                    </div>
                    ''', unsafe_allow_html=True)
                    
            except Exception as e:
                st.markdown(f'''
                <div style="background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 1rem; border-radius: 8px;">
                    ❌ Error en los cálculos: {str(e)}
                </div>
                ''', unsafe_allow_html=True)
                
        else:
            st.markdown('''
            <div style="background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; padding: 1rem; border-radius: 8px; text-align: center;">
                ⚠️ Introduce los valores de superficie, goteros totales y caudal del gotero para ver los cálculos
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer with instructions
    st.markdown("""
    <div class="info-section" style="margin-top: 2rem;">
        <h4 style="color: #1976D2; margin-top: 0;">ℹ️ Instrucciones de uso</h4>
        <ol style="margin: 1rem 0;">
            <li>Introduce todos los datos de entrada en los campos de la izquierda</li>
            <li>Los cálculos se actualizarán automáticamente</li>
            <li>El resultado final del abono gastado aparecerá cuando todos los campos estén completos</li>
            <li>Usa los botones para guardar en PDF, compartir o reiniciar</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    if numero_invernadero:
        st.markdown(f"""
        <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; border-left: 4px solid #4CAF50; margin-top: 1rem;">
            <strong>🏠 Invernadero:</strong> {numero_invernadero}
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
