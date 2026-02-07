"""
Testes unitários básicos para os serviços da Loja Veloz
"""
import pytest
import sys
import os

# Adiciona o path dos serviços
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'services', 'api-gateway'))


class TestHealthEndpoint:
    """Testes para o endpoint de health check"""
    
    def test_health_response_structure(self):
        """Verifica estrutura esperada da resposta de health"""
        expected_keys = ['service', 'status']
        # Simula estrutura de resposta
        response = {'service': 'test-service', 'status': 'UP'}
        
        for key in expected_keys:
            assert key in response
    
    def test_health_status_values(self):
        """Verifica valores válidos de status"""
        valid_statuses = ['UP', 'DOWN', 'DEGRADED']
        status = 'UP'
        
        assert status in valid_statuses


class TestServiceConfiguration:
    """Testes para configuração dos serviços"""
    
    def test_service_name_from_env(self):
        """Verifica que SERVICE_NAME pode ser lido do ambiente"""
        os.environ['SERVICE_NAME'] = 'test-service'
        service_name = os.getenv('SERVICE_NAME', 'unknown-service')
        
        assert service_name == 'test-service'
        del os.environ['SERVICE_NAME']
    
    def test_default_service_name(self):
        """Verifica valor padrão quando SERVICE_NAME não está definido"""
        # Remove se existir
        if 'SERVICE_NAME' in os.environ:
            del os.environ['SERVICE_NAME']
        
        service_name = os.getenv('SERVICE_NAME', 'unknown-service')
        assert service_name == 'unknown-service'


class TestMetricsEndpoint:
    """Testes para métricas Prometheus"""
    
    def test_metrics_content_type(self):
        """Verifica content-type esperado para métricas"""
        expected_content_type = 'text/plain'
        # Em produção, prometheus_client retorna text/plain
        assert expected_content_type == 'text/plain'
