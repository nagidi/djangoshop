from fedex.config import FedexConfig
from fedex.services.rate_service import FedexRateServiceRequest
from fedex.tools.conversion import sobject_to_dict
from fedex.tools.conversion import sobject_to_json
CONFIG_OBJ = FedexConfig(key='hcVXAs60Ralwrw4L',
                         password='Test0987654321',
                         account_number='510087100',
                         meter_number='114090483')
rate = FedexRateServiceRequest(CONFIG_OBJ)

rate.RequestedShipment.DropoffType = 'REGULAR_PICKUP'
rate.RequestedShipment.ServiceType = 'FEDEX_GROUND'
rate.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

rate.RequestedShipment.Shipper.Address.StateOrProvinceCode = 'SC'
rate.RequestedShipment.Shipper.Address.PostalCode = '29631'
rate.RequestedShipment.Shipper.Address.CountryCode = 'US'

rate.RequestedShipment.Recipient.Address.StateOrProvinceCode = 'NC'
rate.RequestedShipment.Recipient.Address.PostalCode = '27577'
rate.RequestedShipment.Recipient.Address.CountryCode = 'US'

rate.RequestedShipment.EdtRequestType = 'NONE'
rate.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

package1_weight = rate.create_wsdl_object_of_type('Weight')
package1_weight.Value = 1.0
package1_weight.Units = "LB"
package1 = rate.create_wsdl_object_of_type('RequestedPackageLineItem')
package1.Weight = package1_weight
package1.PhysicalPackaging = 'BOX'
package1.GroupPackageCount = 1
rate.add_package(package1)

rate.send_request()